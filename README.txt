INSTRUCCIONES DE EJECUCIÓN - ROS 2 TURTLESIM Grupo 2 -
g02_prii3_turtlesim

1.  DESCARGAR EL PROYECTO

Clonar el repositorio:

    git clone https://github.com/VictorCasCat/Proyectos3.git

Entrar en la carpeta descargada:

    cd Proyectos3

2.  COMPILAR EL PROYECTO

Desde la carpeta Proyectos3 ejecutar:

    colcon build

Cuando termine la compilación:

    source install/local_setup.bash

3.  EJECUTAR TURTLESIM

Ejecutar el launch:

    ros2 launch g02_prii3_turtlesim turtlesim_launch.py

Se abrirá TurtleSim y la tortuga comenzará a dibujar automáticamente el
número 2.

4.  SERVICIOS

Para controlar el dibujo, abrir una segunda terminal y entrar en la
carpeta del proyecto:

    cd Proyectos3

Cargar el workspace:

    source install/local_setup.bash

DETENER EL DIBUJO:

    ros2 service call /detener std_srvs/srv/Trigger

La tortuga se detiene en la posición actual.

REANUDAR EL DIBUJO:

    ros2 service call /reanudar std_srvs/srv/Trigger

La tortuga continúa desde el punto en el que se había detenido.

REINICIAR EL DIBUJO:

    ros2 service call /reiniciar std_srvs/srv/Trigger

La pantalla se limpia, la tortuga vuelve a su posición inicial y el
dibujo comienza de nuevo.

5.  RESUMEN RÁPIDO

Terminal 1:

    git clone https://github.com/VictorCasCat/Proyectos3.git
    cd Proyectos3
    colcon build
    source install/local_setup.bash
    ros2 launch g02_prii3_turtlesim turtlesim_launch.py

Terminal 2:

    cd Proyectos3
    source install/local_setup.bash

Para controlar la tortuga:

    ros2 service call /detener std_srvs/srv/Trigger
    ros2 service call /reanudar std_srvs/srv/Trigger
    ros2 service call /reiniciar std_srvs/srv/Trigger
