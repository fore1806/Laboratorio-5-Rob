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

Se procedió a generar diferentes funciones con el fin de generar las trayectorias de cada una de las rutinas solicitadas, estas funciones se listan a continuación
```MATLAB
[xT, yT] = triEq(xiT,yiT,Len,N);

[xC, yC] = circleDiscrete(xCC,yCC,R,30);

[xL, yL] = FINLetter(xF,yF,20,N);

[xP, yP] = Parallel(160,Largo/2,s,Largo,N);

[xDots, yDots] = Dots(120,-120,20,5);


```


### Resultados
![](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/Resultado%20rutinas.jpeg) 

![](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/Trayectoria%20Libre.jpeg) 


![](https://github.com/fore1806/Laboratorio-5-Rob/blob/master/DIAGRAMAS-FOTOS/Resultado%20figura%20libre.jpeg) 
