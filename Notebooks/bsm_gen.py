from collections import deque
from itertools import cycle
import random
from lgsvl.geometry import Vector
import lgsvl.utils

# All coordinates in the API return values in the Unity coordinate system. 
# This coordinate system uses meters as a unit of distance and is a left-handed coordinate system - 
# x points left, z points forward, and y points up.

###
#
# These are the fields used in BSM message
#
###
BSM_PART_1_FIELDS = [
    'msgCnt', # Done
    'id', # Done
    'secMark', # Done
    'latPos',  # Done
    'longPos', # Done
    'elev',    # Done
    'semiMajor', # Not implemented
    'semiMinor', # Not implemented
    'orientation', # Not implemented
    'tranmission', # Not implemented
    'heading', # Done
    'speed', # Done
    'angle', # Not implemented
    'longAccel', # TODO
    'latAccel', # TODO
    'vertAccel', # TODO
    'yawRate', # TODO
    'wheelBrakes', # ?
    'traction', # ?
    'abs', # Not implemented
    'scs', # Not implemented
    'brakeBoost', # Some threshold probably needed, or keep track of 'braking' history. Also, same problem as angle?
    'auxBrake', # AuxBrake, question on access due to VehicleControl
    'width', # TODO, look at bounding box
    'length' # TODO, look at bounding box
]

class BasicSafetyMessage:
    __slots__ = BSM_PART_1_FIELDS
    def __init__(self, **kwargs):
        # Iterate through each field and set to None
        for field in self.__slots__:
            setattr(self, field, kwargs.setdefault(field, None))

    @classmethod
    def to_json(bsm):
        return json.dumps(bsm.__dict__)

def BSM_part_1_gen(agent):
    states = deque(maxlen=2)
    times = deque(maxlen=2)
    message_count_gen = cycle(range(127))
    msg_id = random.randint(0, 2**32-1)
    states.appendleft(agent.state)
    states.appendleft(agent.state)
    times.appendleft(agent.simulator.current_time)
    times.appendleft(agent.simulator.current_time)

    while True:
        bsm = BasicSafetyMessage()
        gps_data = agent.simulator.map_to_gps(states[0].transform)

        # A sequence number within a stream of messages with the same DSRC msgID and from the same sender.
        bsm.msgCnt = next(message_count_gen)
        
        # 4 octet random device identifier. Changes periodically to ensure the overall anonymity of the vehicle
        bsm.id = msg_id

        # Represents the milliseconds within a minute –units of milliseconds
        bsm.secMark = int((agent.simulator.current_time % 1) * 1000)

        # The geographic latitude of an object, expressed in 1/10th integer microdegrees
        bsm.latPos = int(gps_data.latitude * 10_000_000)
        # The geographic longitude of an object, expressed in 1/10th integer microdegrees
        bsm.longPos = int(gps_data.longitude * 10_000_000)
        # Geographic position above or below the reference ellipsoid (typically WGS-84). The number has a resolution of 1 decimeter
        bsm.elevation = int(gps_data.altitude * 10)

        # Not implemented
        bsm.semiMajor = 0
        bsm.semiMinor = 0
        bsm.orientation = 0 # This is the orientation of the ellipsoid, not the vehicle

        # current state of the vehicle transmission
        bsm.transmission = 7 # Enumerated value, transmission is 'unavailable', so 7 is used

        # vehicle speed expressed in unsigned units of 0.02 meters per second
        bsm.speed = (agent.speed // 0.02)
        #current heading of the sending device, expressed in unsigned units of 0.0125 degrees from North
        bsm.heading = (gps_data.orientation % 360) // 0.0125
        # The angle of the driver’s steering wheel, with LSB units of 1.5 degrees, +127 to be used for unavailable
        bsm.steering = 127

        # Signed acceleration of the vehicle along some known axis in units of 0.01 meters per second squared along the Vehicle Longitudinal axis
        bsm.longAccel = (agent_forward * translational_acc) // 0.01
        # Signed acceleration of the vehicle along some known axis in units of 0.01 meters per second squared along the Vehicle Lateral axis
        bsm.latAccel = (agent_left * translational_acc) // 0.01
        # Signed vertical acceleration of the vehicle along the vertical axis in units of 0.02 G
        bsm.vertAccel = (agent_up * translational_acc) // 0.02

        # Yaw Rate of the vehicle, a signed value (to the right being positive) expressed in 0.01 degrees per second
        bsm.yawRate = -1 * states[0].angular_velocity.x

        # 'wheelBrakes', # ?
        # 'traction', # ?
        # 'abs', # Not implemented
        # 'scs', # Not implemented
        # 'brakeBoost', # Some threshold probably needed, or keep track of 'braking' history. Also, same problem as angle?
        # 'auxBrake', # AuxBrake, question on access due to VehicleControl
        
        'width', # TODO, look at bounding box
        'length' # TODO, look at bounding box

        yield bsm


        states.appendleft(agent.state)
        times.appendleft(agent.simulator.current_time)
        agent_forward = lgsvl.utils.transform_to_forward(states[0].transform)
        agent_forward = agent_forward / agent_forward.magnitude() # Get unit vector

        agent_up = lgsvl.utils.transform_to_up(states[0].transform)
        agent_up = agent_up / agent_up.magnitude()

        agent_left = -1 * lgsvl.utils.transform_to_right(states[0].transform) # Make if left to match unity coord system
        agent_left = agent_left / agent_left.magnitude()

        # Translational/Rotational acceleration
        try:
            translational_acc = (states[0].velocity - states[1].velocity) / (times[0] - times[1])
            rotational_acc = (states[0].angular_velocity - states[0].angular_velocity) / (times[0] - times[1])
        except ZeroDivisionError:
            translational_acc = Vector(x=0, y=0, z=0)
            rotational_acc = Vector(x=0, y=0, z=0)
