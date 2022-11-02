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
    radio = 70 *np.sqrt(2)
    angleI = np.pi/32
    x=radio*np.cos(angleI)
    y=-radio*np.cos(angleI)
    z=70
    q0 = [0,0,0,0,-0.15]
    q10 = phinv(x,y,z+30,-0.15)
    q1 = phinv(x,y,z,-0.15)
    #q2 = [q1[0]+np.pi/4,q1[1],q1[2],q1[3],-0.15]
    q3 = [q1[0]+2*np.pi/3,q1[1],q1[2],q1[3],-0.15]
    q4 = [q1[0]+2*np.pi/3,q1[1]+np.pi/6,q1[2],q1[3],-0.15]
    return [list(q0),list(q10),list(q1),list(q3),list(q4),list(q0)]

def rangoMax():
    radio = 215*np.sqrt(2)
    angleI = np.pi/8
    x=radio*np.cos(angleI)
    y=-radio*np.cos(angleI)
    z=80
    q0 = [0,0,0,0,-0.15]
    q10 = [-0.873,-0.838,0.954,0.059,-0.15]#phinv(x,y,z,-0.15)
    q1 = [-0.873,-0.917,0.914,0.177,-0.15]#phinv(x,y,z,-0.15)
    q2 = [0.873,-0.869,0.917,0.127,-0.15]
    q20 = [0.873,-0.869+np.pi/6,0.917,0.127,-0.15]
    return [list(q0),list(q10),list(q1),list(q2),list(q20),list(q0)]


 #################### LECTURA TRAYECTORIAS ####################
raw_data = open('qDots.csv')
qDots = np.loadtxt(raw_data, delimiter=",")

raw_data = open('qCircle.csv')
qCircle = np.loadtxt(raw_data, delimiter=",")

raw_data = open('qDejado.csv')
qDejado = np.loadtxt(raw_data, delimiter=",")

raw_data = open('qLetter.csv')
qLetter = np.loadtxt(raw_data, delimiter=",")

raw_data = open('qPar.csv')
qPar = np.loadtxt(raw_data, delimiter=",")

raw_data = open('qRecolecccion.csv')
qRecoleccion = np.loadtxt(raw_data, delimiter=",")

raw_data = open('qTriangle.csv')
qTriangle = np.loadtxt(raw_data, delimiter=",")

#Libre

raw_data = open('qCircle2.csv')
qCircle2 = np.loadtxt(raw_data, delimiter=",")


 #################### FIN LECTURA TRAYECTORIAS ####################




def joint_publisher():
    pub = rospy.Publisher('/joint_trajectory', JointTrajectory, queue_size=0)
    rospy.init_node('joint_publisher', anonymous=False)

 
    
    while not rospy.is_shutdown():

        

       key=input()
        if(reec==0 and (key != 'z' or key != 'Z') :
            key=' '
        if key == 'z' or key == 'Z':
            llamado=qRecoleccion
            reec==1
            indice = 0
            key = ' '
        elif key == 'x' or key == 'X':
            llamado=qTriangle
            indice = 
            key = ' '
        elif key == 'c' or key == 'C':
            llamado=qLetter
            indice = 2
            key = ' '
        elif key == 'v' or key == 'V':
            llamado=qCircle
            indice = 3
            key = ' '
        elif key == 'b' or key == 'B':
            llamado=qDots
            key = ' '
        elif key == 'l' or key == 'L':
            llamado=qPar
        elif key == 'd' or key == 'D':
            llamado=qDejado
            reec==0
        elif key == 'n' or key == 'N':
            llamado = rangoMin()
            key = ' '
        elif key == 'm' or key == 'M':
            llamado = rangoMax()
            key = ' '
        elif key == 'f' or key == 'F':
            llamado = qCircle2
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
            rospy.sleep(3)
            print('\n') 


termino = True 

if __name__ == '__main__':
    try:
        joint_publisher()

    except rospy.ROSInterruptException:
        pass