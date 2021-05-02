# AVSurvivability-Python

This repo contains files related to experimenting with the PythonAPI for LGSVL.

## Goals
- Learn how to, in general, use LGSVL
- Provide BSM generation in LGSVL.
- Create functionality for simpler custom scenario generation

## Summary Results
- Learned a lot about the general workflow and how LGSVL works. This extends much past the PythonAPI. I would estimate 70% of the workload was reading source code and documentation from both the PythonAPI and the entire LGSVL simulator.
- A rudimentary BSM generator was created, but with many compromises due to the limitations of the PythonAPI. The problems are described in more detail below.
- Functionality for basic scenario creation was made late in the process. However, a new version of the LGSVL simulator was released which provided an easier way to do this. So work on that task was halted.
- The new release also provided an easier way for us to share assets in Unity. Because of the issues faced with the PythonAPI, we decided to stop using it for our current goals. We have since switched to using Unity to build game assets, allowing for finer control and easier sharing.

## Things I'd have done differently
- Most of the programming was using the `jupyter notebook` Python interpreter or `ipython`, which allowed for fast and easy live testing of new ideas. However it also meant that I didn't have an easy way to save or version control my progress as most of it was discarded immediately by the interpreter. This ultimately led to fewer programming artifacts to refer to after a session of testing code. This resulted in easy short term testing but more difficult long term testing. If I continue to use similar tools in the future I know I need to make a conscious effort to maintain version control.
- I would have contacted the LGSVL team for guidance earlier than I did. There were some misunderstandings of what the API's intended purpose was which led to additional difficulties. Had we have spoken to them earlier we may have switched to using Unity much earlier, reducing the amount of unused development time.

## Other comments

A good portion of the time was spent learning how to use the API in general. Once I built understanding I worked on implementing a BSM generator using the API.

In the aftermath, we realized that using the Python API for BSM generation was not ideal. The API presented limited information about the simulator state and the simulator had to be paused when polling data. When we ran into issues, we had made an Issue on the LGSVL GitHub page, and the developers warned that the Python API was not explicitly intended for real-time polling of sensor data.

Despite this we created a semi-functional BSM generator, though the limitations they mentioned were apparent. They simulator had to be stopped every 100ms to generate the data, causing the simulation to feel very choppy. Also, some of the directional data seemed to be nonsensical. After some debugging this was traced back to the fact that some data used left-handed unit vectors and some used right-handed unit vectors. The code in the Python API that performed the matrix operations was uncommented, which would have made the process of fixing this more complicated. 

Around this time SVL 2021.1 was released which introduced online sharing of custom Unity assets. With the challenges we were facing and the new possibilities presented, we opted to switch to developing the BSM generator using Unity. This meant we had lost some progress but it give us a more streamlined approach of developing and sharing the software we would create.
