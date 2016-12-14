from objects_common.jsonObject import JsonObject
from objects_common.enumType import EnumType

class EdgeEnd(JsonObject):

    def __init__(self, json_struct=None):
        self.switchingCap=Switchingcap(0)
        self.edgeEndId=""
        self.name=""
        self.peerNodeId=""
        super(EdgeEnd, self).__init__(json_struct)

class Switchingcap(EnumType):
    possible_values = ['lsc', 'psc']
    range_end = 2

    def __init__(self, initial_value):
        super(Switchingcap, self).__init__(initial_value)
