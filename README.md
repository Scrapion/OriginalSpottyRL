# Gazebo-Simulation
In questa repo ci sono le simulazioni per robot fatte utilizzando Gazebo 

# Panoramica

In questa repository, sto caricando i modelli URDF dei robot e le loro simulazioni realizzate con Gazebo.

Gli ambienti sono strutturati come spazi di lavoro catkin in un ambiente ROS Noetic su Ubuntu 20.04. Il software potrebbe non funzionare o non essere compilato al di fuori di questo ambiente.

È possibile utilizzare il sistema di compilazione ROS Catkin make, ma è preferibile utilizzare catkin tools. I comandi di compilazione riportati di seguito saranno forniti assumendo catkin tools.



## Installazione

Puoi installare Ros Noetic tramite le istruzioni a questo link:

https://wiki.ros.org/noetic/Installation/Ubuntu

Durante l'installazione di ROS è consigliabile installare i seguenti packages: 
```
sudo apt-get install ros-noetic-joy
sudo apt-get install ros-noetic-rplidar-ros
sudo apt-get install ros-noetic-hector-slam
sudo apt-get install ros-noetic-teleop-twist-keyboard
```

Per quanto riguarda catkin tools utilizza questi comandi:

```
sudo apt-get install python3-catkin-tools
sudo apt-get install python3-catkin-pkg python3-catkin-pkg-modules
```

## Lancio della macchinina
Dopo aver scaricato la repo ed aver estratto il contenuto su Home (non obbligatorio ma preferibile), 
Apri la directory sorcio_2_ws nel terminale e lancia i seguenti comandi:
```
catkin build

source devel/setup.bash

roslaunch test_description gazebo.launch
```

Se vuoi provare a controllare la macchinina tramite la tastiera, su un altro terminale lancia il seguente comando:
```
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```

Se vuoi avere anche una visione "migliore" di ciò che sta succedendo attorno al robot (riguardo alla sensoristica), lancia anche questo comando in un altro terminale:
```
cd sorcio_2_ws

source devel/setup.bash

roslaunch test_description display.launch
```


