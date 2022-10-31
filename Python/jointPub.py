from asyncore import poll3
from re import sub
import rospy
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


def phinv(x, y, z, q5):
    #Triangulo constante
    hipo=106.5; #distancia diagonal entre q2 y q3
    cate=np.sqrt(hipo**2-100**2) #cateto de la diagonal
    angle = np.arctan2(cate,100)
    
    q1=np.arctan2(y,x)
    
    dmar0 = np.array([[x], [y], [z]])
    d3 = np.multiply(np.array([[np.cos(q1)], [np.sin(q1)], [0]]),100)
    dw0 = dmar0-d3
    
    dz = dw0[2]-94
    r2 = (dw0[0])**2+(dw0[1])**2+(dz)**2
    r = np.sqrt(r2)
    
    #Teorema del coseno
    alpha = np.arccos((100**2+r2-hipo**2)/(2*r*100))
    beta = np.arccos((r2+hipo**2-100**2)/(2*r*hipo))
    gamma = np.arccos((hipo**2+100**2-r2)/(2*hipo*100))

    theta = np.arctan2(dz,np.sqrt((dw0[0])**2+(dw0[1])**2))
    psi = np.pi-alpha
    phi = np.pi-psi-theta
    omega = np.pi-phi
    kappa = omega-np.pi/2
    
    q2= np.round(np.pi/2-theta-beta-angle-np.pi/18,3)
    q3= np.round(np.pi-gamma-(np.pi/2-angle),3)
    q4 =np.round(-(np.pi/2-kappa),3)

    return [float(np.round(q1,3)),float(-q2),float(-q3),float(-q4),float(q5)]

def rangoMin():
    x=100
    y=-100
    z=120
    q0 = [0,0,0,0,-0.15]
    q1 = phinv(x,y,z,-0.15)
    q2 = [q1[0]+np.pi/4,q1[1],q1[2],q1[3],-0.15]
    q3 = [q2[0]+np.pi/4,q2[1],q2[2],q2[3],-0.15]
    return [list(q0),list(q1),list(q2),list(q3),list(q0)]

def rangoMax():
    x=200
    y=-200
    z=120
    q0 = [0,0,0,0,-0.15]
    q1 = phinv(x,y,z,-0.15)
    q2 = [q1[0]+np.pi/4,q1[1],q1[2],q1[3],-0.15]
    q3 = [q2[0]+np.pi/4,q2[1],q2[2],q2[3],-0.15]
    return [list(q0),list(q1),list(q2),list(q3),list(q0)]

def circle(x, y, z, r):
    n = 361 #Número de puntos
    qCircle = np.zeros((n,5))
    for i in range (n):
        xq = x+r*np.cos(np.deg2rad(i))
        yq = y+r*np.sin(np.deg2rad(i))
        qCircle[i] = phinv(xq,yq,z,-0.15)
    return qCircle

def eqTriangle(x,y,z,l):
    n=5
    #qTriangle = np.zeros((3*(n),5))
    q000 = [0,0,0,0,-0.15]
    q0s = phinv(x,y,z+100,-0.15)
    bajar= phinv(x,y,z,-0.15)
    #q1s = line(x,y,x+l,y,z)
    #q2s = line(x+l,y,x+l-l*np.cos(np.pi/3),y+l*(np.pi/3),z)
    #q3s = line(x+l-l*np.cos(np.pi/3),y+l*(np.pi/3), x, y,z)
    #subir = phinv(x,y,z+20,-0.15)

    #lenT = len(q1s)+len(q2s)+len(q3s)+3

    q1s = phinv(x+60,y,z,-0.15)
    q2s = phinv(x+30,y+50,z,-0.15)
    q3s = phinv(x,y,z,-0.15)
    q4s = phinv(x,y,z+100,-0.15)
    #qTriangle1 = np.concatenate(np.concatenate((q1s,q2s)),q3s)
    qTriangle = [list(q000),list(q0s),list(bajar),list(q1s),list(q2s),list(q3s),list(q4s),list(q000)]
    #for i in range (3):
    #    for j in range (n):
    #        if i == 0:
    #            x = x + (l/(n-1))
    #        elif i == 1:
    #            x = x - (l/(n-1))*np.cos(np.pi/3)
    #            y = y + (l/(n-1))*np.sin(np.pi/3)
    #        elif i==2:
    #            x = x - (l/(n-1))*np.cos(np.pi/3)
    #            y = y - (l/(n-1))*np.sin(np.pi/3)
    #    qTriangle[i*(n-1)+j] = phinv(x,y,z,-0.15)
    return qTriangle

def parallel(x,y,z,l,k,P):
    n = 101
    # k número de líneas
    # P -> 0 si es horizontal; 1 si es vertical
    qLine = np.zeros((k*(n-1)+3*k,5))

    for i in range(k):
        for j in range(n):
            if P==0: #Horizontales
                if (i%2==0):
                    x = x + (l/(n-1))
                else:
                    x = x - (l/(n-1))
            else:
                if (i%2==0):
                    y = y - (l/(n-1))
                else:
                    y = y + (l/(n-1))
            qLine[i*(n-1)+i*(k-1)+j] = phinv(x,y,z,-0.15)

        if(i<k-1):
            qLine[(i+1)*(n-1)] = phinv(x,y,z+20,-0.15)
            if P == 0:
                y = y-20
            else:
                x = x+20
            qLine[(i+1)*(n-1)+1] = phinv(x,y,z+20,-0.15)
            qLine[(i+1)*(n-1)+2] = phinv(x,y,z,-0.15)

    return qLine

def line(xi,yi,xf,yf,z):
    n = 3
    angle = np.arctan2((yf-yi),(xf-xi))
    dist = np.sqrt((yf-yi)**2+(xf-xi)**2)
    qLines = np.zeros((n,5))
    x = xi
    y =yi
    for i in range (n):
        x = x + (dist/(n-1))*np.cos(angle)
        y = y + (dist/(n-1))*np.sin(angle)
        qLines[i] = list(phinv(x,y,z,-0.15))
    return qLines

def FLetter(x,y,z):
    xArray = np.Array([x, x, x+10, x, x, x+10])
    yArray = np.ArrAY([y, y+10, y+10, y+10, y+20, y+10])
    qFL = np.array([[line(xArray[0],yArray[0],xArray[1],yArray[1],z)],[line(xArray[1],yArray[1],xArray[2],yArray[2],z)],[line(xArray[2],yArray[2],xArray[3],yArray[3],z)],[line(xArray[3],yArray[3],xArray[4],yArray[4],z)],[line(xArray[4],yArray[4],xArray[5],yArray[5],z)]])
    return qFL

def ILetter(x,y,z):
    qIL = np.array([line(x,y,x,y+20,z)])
    return qIL

def NLetter(x,y,z):
    xArray = np.Array([x, x, x+10, x+10])
    yArray = np.ArrAY([y, y+20, y, y+20])
    qNL = np.array([[line(xArray[0],yArray[0],xArray[1],yArray[1],z)],[line(xArray[1],yArray[1],xArray[2],yArray[2],z)],[line(xArray[2],yArray[2],xArray[3],yArray[3],z)]])
    return qNL

def Letras(x,y,z):
    FArray = FLetter(x,y,z)
    sube1 = phinv(x+10,y+20,z+20,-0.15)
    mov1 = line(x+10,y+20,x+15,y,z+20)
    baja1 = phinv(x+15,y,z,-0.15)
    IArray = ILetter(x+15,y,z)
    sube2 = phinv(x+15,y+20,z+20,-0.15)
    mov2 = line(x+15,y+20,x+20,y,z+20)
    baja2 = phinv(x+20,y,z,-0.15)
    NArray = NLetter(x+20,y,z)
    letrasq=np.array([[FArray],[sube1],[mov1],[baja1],[IArray],[sube2],[mov2],[baja2],[NArray]])
    return letrasq

def points(x,y,z,dis):
    n=5
    puntos=np.zeros((3*n,5))
    for i in range(5):
        puntos[i*3]= phinv(x+i*dis,y,z+10,-0.15)
        puntos[i*3+1]= phinv(x+i*dis,y,z,-0.15)
        puntos[i*3+2]== phinv(x+i*dis,y,z+10,-0.15)
    return puntos





def joint_publisher():
    pub = rospy.Publisher('/joint_trajectory', JointTrajectory, queue_size=0)
    rospy.init_node('joint_publisher', anonymous=False)

 
    
    while not rospy.is_shutdown():

        

        key=input()
        if key == 'z' or key == 'Z':
            #p1 = phinv(150,150,100,-0.15)
            #p2 = phinv(250,200,100,-0.15)
            #p3 = phinv(180,180,100,-0.15)
            #llamado=np.array([list(p1),list(p2),list(p3)])
            #llamado = triangulo
            llamado = triangulo
            indice = 0
            key = ' '
        elif key == 'x' or key == 'X':
            indice = 1
            key = ' '
        elif key == 'c' or key == 'C':
            indice = 2
            key = ' '
        elif key == 'v' or key == 'V':
            indice = 3
            key = ' '
        elif key == 'b' or key == 'B':
            indice = 4
            key = ' '
        elif key == 'n' or key == 'N':
            llamado = rangoMin()
            key = ' '
        elif key == 'm' or key == 'M':
            llamado = rangoMax()
            key = ' '
        else:
            p1 = [0,0,0,0,-0.15]
            p2 = [0,0,0,0,-0.15]
            llamado=np.array([list(p1),list(p2)])
            key = ' '

        for i in range (len(llamado)):
            state = JointTrajectory()
            state.header.stamp = rospy.Time.now()
            state.joint_names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5"]
            point = JointTrajectoryPoint()
            point.positions = llamado[i]
            point.time_from_start = rospy.Duration(0.5)
            state.points.append(point)
            pub.publish(state)
            print(llamado[i])
            print('published command \n')
            rospy.sleep(5)
        #print(llamado[i])
            print('\n') 


#circulo = circle(150,150,100,100)
triangulo = eqTriangle(150,150,120,50)#line(150,150,120,120,100)#eqTriangle(150,150,120,50)
termino = True 
print(triangulo) 

print(rangoMin())
#paralelas = parallel(200,200,70,50,2,0)
#iniciales = Letras(150,150,70)
#puntos = points(180,180,50,15)

if __name__ == '__main__':
    try:
        #llamado = triangulo
        #for i in range(len(llamado)):
        joint_publisher()

    except rospy.ROSInterruptException:
        pass