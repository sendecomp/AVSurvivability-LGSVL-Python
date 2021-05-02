from abc import ABC, abstractmethod, abstractmethod
import lgsvl
import os

"""
Barebones wrapper for scripting and packaging custom scenarios using the PythonAPI

While the basic functionality worked, it never was completed because we SVL 2021.1 was released before this was needed.
That version provided the Visual Scenario Editor, provides a graphical mode of 
creating scenarios, which would be easier than this would have been.
"""

class Scenario(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def reset(self):
        raise NotImplementedError()

    @abstractmethod
    def run(self, iterations=None):
        raise NotImplementedError()

class DriveForward(Scenario):
    def __init__(self, *args, **kwargs):
        self.name = 'DriveForward'
        self.simulator_host = kwargs.setdefault('SIMULATOR_HOST', '127.0.0.1')
        self.simulator_port = kwargs.setdefault('lgsvl_port', 8181)
        self.ego = None
        self.reset()

    def reset(self):
        """
        Resets to the initial state of the scenario
        """
        # Loads the named map in the connected simulator. The available maps can be set up in web interface
        if sim.current_scene == "BorregasAve":
            sim.reset() 
        else:
            sim.load("BorregasAve")

        # Get a state from the simulator and spawn a vehicle
        spawns = sim.get_spawn()
        state = lgsvl.AgentState()
        state.transform = spawns[0]

        sim.load('BorregasAve')

        forward = lgsvl.utils.transform_to_forward(spawns[0])

        # Agents can be spawned with a velocity. Default is to spawn with 0 velocity
        state.velocity = 20 * forward
        self.ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)
