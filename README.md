# Quinto Laboratorio - Cinemática Inversa - Phantom X - ROS :robot: 
 
Quinto laboratorio de la asignatura Robótica de la Universidad Nacional de Colombia en su sede Bogotá. 
 
## Autores :busts_in_silhouette: 
 
|               Nombre               |GitHub nickname| 
|------------------------------------|---------------| 
|  Nikolai Alexander Caceres Penagos |[nacaceresp](https://github.com/nacaceresp)| 
|     Andrés Felipe Forero Salas     |[fore1806](https://github.com/fore1806)| 
|  Iván Mauricio Hernández Triana    |[elestrategaactual](https://github.com/elestrategaactual)|

## Introducción

La mayor parte de las aplicaciones de la robótica se basan en establecer trayectorias requeridas para un manipulador dentro de su espacio de trabajo, definiendo diversas posturas del mismo a través de conocer la posición de su herramienta de trabajo, asi como la orientación de la misma. De esta forma, el problema cinemático inverso, se encarga de establecer las posiciones articulares del manipulador, permitiendo su control desde un entorno de desarrollo software.

## Solución planteada

### Modelo Cinemático Inverso

Para el módelo cinemático inverso del manipulador Phantom X Pincher en la versión más actualizada con la que cuenta el Laboratorio de Sistemas Robotizados (LabSIR) de la Universidad Nacional de Colombia, se utilizo el método geométrico teniendo en cuenta la orientacion que el efector final debia mantener para el proceso de escritura. Este procedimiento se encuentra explicado a detalle en el archivo livescript [PhantomInverse](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/MATLAB/PhantomInverse.mlx).

### Configuración inicial Dynamixel Workbench y entorno ROS

Para la configuración inicial del entorno de trabajo, se utilizó un procedimiento análogo al expuesto en el repositorio [Laboratorio-4-Rob](https://github.com/fore1806/Laboratorio-4-Rob.git). Comenzando por clonar el repositorio de GitHub [dynamixel_one_motor](https://github.com/fegonzalez7/dynamixel_one_motor.git) dentro de la carpeta creada de ***catkin_ws_lab_5*** y se siguieron los pasos especificados en el README, teniendo en cuenta que previo a lanzar el controlador de los motores del Phantom X, hacia falta una línea de comando como se muestra a continuación.

```
    catkin build dynamixel_one_motor
    source devel/setup.bash
    roslaunch dynamixel_one_motor one_controller.launch
```

### Código Solución

Para desarrollar la solución del laboratorio, el equipo de trabajo se basó en el anterior repositorio remoto conjuntamente con el repositorio [px_robot](https://github.com/felipeg17/px_robot.git), comenzando por utilizar el archivo [joint.yaml](https://github.com/felipeg17/px_robot/blob/master/config/joints.yaml) renombrado como [basic.yaml](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/catkin_ws_Lab_5/src/dynamixel_one_motor/config/basic.yaml).

Se procedió a generar diferentes funciones en MATLAB con el fin de generar las trayectorias de cada una de las rutinas solicitadas ,este procedimiento se encuentra explicado a detalle en el archivo livescript [Trayectorias](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/MATLAB/trayectorias.mlx).
, adicional a esto se definió el punto de recolección de la herramienta y se generó una rutina de acercamiento sujeción con el gripper y posteriormente regreso al punto de espera y para regresarla se encontró que la rutina anterior cumplía con esta tarea también en caso de ser invertida; estas funciones se listan a continuación:
```MATLAB
[xT, yT] = triEq(Xi,Yi,Len,N);

[xC, yC] = circleDiscrete(xCC,yCC,R,N);

[xL, yL] = FINLetter(Xi,Yi,H,N);

[xP, yP] = Parallel(Xi,Yi,d,Largo,N);

[xDots, yDots] = Dots(Xi,yi,d,N);

[r,theta] = trayectoria0(pi/4,80,1,3.5,4,35);

[xFree,yFree] = Totrigen(220,0,theta,r);

[xC3, yC3] = cuadr(200*sqrt(2),0,R,5);

```
Con el uso de esta funciones y utilizando valores iniciales que generara puntos dentro del espacio de trabajo se obtuvieron las siguientes trayectorias:


![](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/Trayectorias1.png)

![](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/Trayectoria%20Libre.jpeg) 

Con los puntos de las trayectorias generados se procedió a realizar las transformaciones de estos puntos en el espacio a ángulos articulares con el modelo inverso obtenido previamente adicional a esto se les adiciono que comenzara en el punto de espera que en este caso es el [0,0,0,0] y adicionalmente se generaron puntos de aproximación y de salida los cuales manteniendo la distancia en X y Y alterando unicamente la altura Z.

Posteriormente, los vectores de ángulos articulares generados son almacenados en formato csv mediante los siguientes comandos de MATLAB
```MATLAB
csvwrite('qRecolecccion.csv',qRecoleccion);
csvwrite('qDejado.csv',qDejado);
csvwrite('qTriangle.csv',qTriangle);
csvwrite('qCircle.csv',qCircle);
csvwrite('qLetter.csv',qLetter);
csvwrite('qPar.csv',qPar);
csvwrite('qDots.csv',qDots);
csvwrite('qFree.csv',qFree);
```
Estos datos son cargados en Python mediante los siguientes comandos:
```python
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
```

Una Vez cargados estos vectores se procede a enviarlos al Robot según la solicitud del usuario el cual mediante comandos de texto ingresa la trayectoria que quiere obtener.

| Tecla | Operación                        |
| -- | -- |
|z    | Recolección                      |
|x    | Triangulo  Equilatero            |
|c    | Letras                           |
|v    | Circulo                          |
|b    | Puntos                           |
|l    | Lineas Paralelas                 |
|d    | Dejado                           |
|n    | Rango Minimo                     |
|m    | Rango Máximo                     |
|f    | Figura Libre                     |


```python
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
       
```
A partir de un ciclo for se recorre el arreglo punto a punto para obtener la trayectoria solicitada
```python
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
```

### Resultados
![](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/Resultado%20rutinas.jpeg) 




![](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/Resultado%20figura%20libre.jpeg) 
