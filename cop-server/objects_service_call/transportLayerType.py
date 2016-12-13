from objects_common.jsonObject import JsonObject
from objects_common.enumType import EnumType

class TransportLayerType(JsonObject):

    def __init__(self, json_struct=None):
        self.action=Action(0)
        self.layer=Layer(0)
        self.direction=Direction(0)
        self.layerId=""
        super(TransportLayerType, self).__init__(json_struct)

class Action(EnumType):
    possible_values = ['forward', 'push_tag', 'pop_tag']
    range_end = 3

    def __init__(self, initial_value):
        super(Action, self).__init__(initial_value)
class Layer(EnumType):
    possible_values = ['dwdm_link', 'ethernet', 'ethernet_broadcast', 'mpls']
    range_end = 4

    def __init__(self, initial_value):
        super(Layer, self).__init__(initial_value)
class Direction(EnumType):
    possible_values = ['unidir', 'bidir']
    range_end = 2

    def __init__(self, initial_value):
        super(Direction, self).__init__(initial_value)
