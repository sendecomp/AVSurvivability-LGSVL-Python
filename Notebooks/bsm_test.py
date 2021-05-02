"""
Provides barebones data structure for populating data from the simulator

Intended for use with an interpretter. I am using ipython.
"""

import lgsvl
import json

sim = lgsvl.Simulator("127.0.0.1", 8181)
if sim.current_scene == "BorregasAve":
  sim.reset()
else:
  sim.load("BorregasAve")

spawns = sim.get_spawn()

state = lgsvl.AgentState()
state.transform = spawns[0]

a = sim.add_agent("Jaguar2015XE (No Bridge)", lgsvl.AgentType.EGO, state)

class BasicSafetyMessage:
    def __init__(self, **kwargs):
        self.msgCnt= kwargs.setdefault('msgCnt', None)
        self.id= kwargs.setdefault('id', None)
        self.secMark= kwargs.setdefault('secMark', None)
        self.lat= kwargs.setdefault('lat', None)
        self.long= kwargs.setdefault('los ng', None)
        self.elev= kwargs.setdefault('elev', None)
        self.accuracy= kwargs.setdefault('accuracy', None)
        self.transmission= kwargs.setdefault('transmission', None)
        self.speed= kwargs.setdefault('speed', None)
        self.heading= kwargs.setdefault('heading', None)
        self.angle= kwargs.setdefault('angle', None)
        self.accelSet= kwargs.setdefault('accelSet', None)
        self.brakes= kwargs.setdefault('brakes', None)
        self.size= kwargs.setdefault('size', None)

    @classmethod
    def to_json(bsm):
        return json.dumps(bsm.__dict__)