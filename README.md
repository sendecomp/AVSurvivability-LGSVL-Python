# AVSurvivability-Python

This repo contains files related to experimenting with the PythonAPI for LGSVL.

A good portion of the time was spent learning how to use the API in general. Once I built understanding I worked on implementing a BSM generator using the API.

In the aftermath, we realized that using the Python API for BSM generation was not ideal. The API presented limited information about the simulator state and the simulator had to be paused when polling data. When we ran into issues, we had made an Issue on the LGSVL GitHub page, and the developers warned that the Python API was not explicitly intended for real-time polling of sensor data.

Despite this we create together a semi-functional BSM generator, though the limitations they mentioned were apparent. They simulator had to be stopped every 100ms to generate the data, causing the simulation to feel very choppy. Also, some of the directional data seemed to be nonsensical. After some debugging this was traced back to the fact that some data used left-handed unit vectors and some used right-handed unit vectors. The code in the Python API that performed the matrix operations was uncommented, which would have made the process of fixing this more complicated. 

Around this time SVL 2021.1 was released which introduced online sharing of custom Unity assets. With the challenges we were facing and the new possibilites presented, we opted to switch to developing the BSM generator using Unity. This meant we had lost some progress but it give us a more streamlined approach of developing and sharing the software we would create.
