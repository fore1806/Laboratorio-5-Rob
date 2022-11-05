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
Adicional a esto se definió el punto de recolección de la herramienta y se generó una rutina de acercamiento para la sujeción con el gripper. Finalmente se encontró que la rutina anterior cumplía también con la tarea de dejado en caso de ser invertida; estas funciones se listan a continuación:

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

Con el uso de estas funciones y utilizando valores iniciales que generará los puntos dentro del espacio de trabajo se obtuvieron las siguientes trayectorias:


![](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/Trayectorias1.png)

Adicionalmente, se definió una trayectoria de un trébol estilizado circunscrito en un cuadrado, como se observa en la imagen siguiente.

![](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/Trayectoria%20Libre.jpeg) 

Con los puntos de las trayectorias generados se procedió a realizar las transformaciones de estos puntos en el espacio a ángulos articulares con el modelo inverso obtenido previamente, adicionalmente, se definió el punto de partida en la posición de home [0,0,0,0] y generando puntos de aproximación y de salida los cuales manteniendo la distancia en X y Y alterando unicamente la altura Z.

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


#Libre

raw_data = open('qCircle2.csv')
qCircle2 = np.loadtxt(raw_data, delimiter=",")

#Free

raw_data = open('qFree.csv')
qFree = np.loadtxt(raw_data, delimiter=",")
```

Una Vez cargados estos vectores se procede a enviarlos al Robot según la solicitud del usuario el cual mediante comandos de texto ingresa la trayectoria que quiere obtener, según la siguiente tabla.

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
        inicio = time.time()
        if(reec==0 and (key != 'z' or key != 'Z') :
            key=' '
            print(con herramienta)
        else:
           print(sin herramienta)
        if key == 'z' or key == 'Z':
            llamado=qRecoleccion
            reec==1
            print("Recoleccion")
            key = ' '
        elif key == 'x' or key == 'X':
            llamado=qTriangle
            print("Triangle")
            key = ' '
        elif key == 'c' or key == 'C':
            llamado=qLetter
            print("Letters")
            key = ' '
        elif key == 'v' or key == 'V':
            llamado=qCircle
            print("Circle")
            key = ' '
        elif key == 'b' or key == 'B':
            llamado=qDots
            print("Dots")
            key = ' '
        elif key == 'l' or key == 'L':
            llamado=qPar
            print("Parallel")
        elif key == 'd' or key == 'D':
            llamado=qDejado
            print("Dejado")
            reec==0
        elif key == 'n' or key == 'N':
            llamado = rangoMin()
            print("rangoMin")
            key = ' '
        elif key == 'm' or key == 'M':
            llamado = rangoMax()
            print("rangoMax")
            key = ' '
        elif key == 'f' or key == 'F':
            llamado = qCircle2
            print("Libre")
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
print("Terminado")
print("\n")
print("Tiempo:")
print(time.time()-inicio)
```

### Resultados

En el video de Youtube al que se puede acceder en la siguiente imagen, se observa el manipulador Phantom X, realizando las trayectorias especificadas anteriormente.

[![Alt text](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/Thumbnail.png)](https://youtu.be/NH3ZaQMMAC8)

De la misma forma, en la siguiente imagen se evidencia el resultado final del proceso de dibujo de las trayectorias iniciales.

![](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/Resultado%20rutinas.jpeg)

Asi mismo, en la siguiente imagen se puede visualizar el resultado de la figura libre desarrollada.

![](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/Resultado%20figura%20libre.jpeg)

En estas dos fotografías se puede evidenciar que se presentan algunos errores en el proceso de dibujo, respecto a lo esperado del código de MATLAB, esto se analizará con detalle en la sección subsecuente.

### Análisis

A continuación se presenta el resultado obtenido en la práctica en contraste con lo esperado teóricamente para la figura libre, en base al código de MATLAB.

![](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/TraslapeFiguraLibre.png) 

Como se puede apreciar, en la práctica se obtiene una figura muy parecida a lo que teoricamente se hace por medio de la herramienta de MATLAB; sin embargo, vale la pena resaltar que se presenta en primer lugar, una pequeña desviacion del rango maximo obtenido Vs el esperado, desviacion atribuida al movimiento del marcador a la hora de hacer tal figura, el cual, no se logra inmovilizar en su totalidad. Además, es de notar que el trebol estilizado no posee la suavidad que caracteriza al elaborado en matlab, suavidad que no se logra para la cantidad de puntos graficados. Por último, se ve una figura más pequeña conforme se acerca al rango minimo, diferencia que puede ser atribuida a un error de captura de la fotografia y al error en si que posee el robot, el cual se evidenció especialmente en la medida que el robot dibujaba cerca a su límite minimo, pues al perder altura en cada uno de los movimientos, se termina obtiendo una figura más pequeña. 

![](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/TraslapeGeneral.png) 

En lo que respecta a la imagen general, se comete un gran error en el momento de tomar la fotografia pues la vista de la misma no es superior sino que se toma con una inclinacion que no favorece a la comparación de la imagen real con la imagen esperada. Es de rescatar la correcta disposición de los puntos, cuyo espaciamiento parece el esperado y la dificultad del robot para realizar trazos paralelos, debido a que no se cuenta con un correcto portaherramientas para el marcador, lo que hace que tenga bastante juego a la hora de dibujar.

Adicionalmente, se observa en las trayectorias cerradas, como el círculo o el triángulo equilatero, el punto final de la trayectoria no coincide apropiadamente con el punto inicial de la misma, a pesar de enviar los mismos valores articulares al manipulador. Lo que nos da un indicio de la repetibilidad del manipulador. Al analizar a detalle estas dos figuras geométricas, se observa que el círculo termina por tomar una forma que se podría describir de mejor manera como elíptica. Por otra parte, respecto al triángulo, a pesar de que su tamaño no es el esperado (lado de 7 cm), se obtuvieron tres líneas que pueden ser catalogadas como rectas. La longitud de estas líneas se reportan en la siguiente tabla.

| Línea | Longitud [cm]   |
| -- | -- |
| base  | 5.86            |
|diag. 1| 5.83            |
|diag. 2| 5.94            |

Finalmente, un evento que cautó especialmente la atención del equipo de trabajo, fue la escritura de las iniciales de los integrantes y especialmente la letra F, pues para reducir operaciones se decidió realizar la F repisando la línea media; sin embargo, al realizar este procedimiento, el manipulador no volvia al punto de partida después de realizar dos veces la misma línea. Al corregir este error desde el código se puede encontrar un valor numérico para la repetibilidad de esta operación de 5 mm.
![](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/error%20en%20F.jpeg)
### Conclusiones

los pincher solo sirven pa mimir
