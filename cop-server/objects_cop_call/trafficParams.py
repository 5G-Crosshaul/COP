from objects_common.jsonObject import JsonObject
from objects_common.enumType import EnumType

class TrafficParams(JsonObject):

    def __init__(self, json_struct=None):
        self.latency=0
        self.OSNR=""
        self.estimatedPLR=""
        self.qosClass=Qosclass(0)
        self.reservedBandwidth=0
        super(TrafficParams, self).__init__(json_struct)

class Qosclass(EnumType):
    possible_values = ['gold', 'silver']
    range_end = 2

    def __init__(self, initial_value):
        super(Qosclass, self).__init__(initial_value)
