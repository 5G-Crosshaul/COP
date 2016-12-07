from objects_common.jsonObject import JsonObject
from node import Node
from edgeEnd import EdgeEnd
from objects_common.enumType import EnumType

class Edge(JsonObject):

    def __init__(self, json_struct=None):
        self.latency=""
        self.name=""
        self.edgeId=""
        self.edgeType=Edgetype(0)
        self.switchingCap=""
        self.metric=""
        self.maxResvBw=""
        self.source=Node() #import
        self.localIfid=EdgeEnd() #import
        self.remoteIfid=EdgeEnd() #import
        self.unreservBw=""
        self.target=Node() #import
        super(Edge, self).__init__(json_struct)

class Edgetype(EnumType):
    possible_values = ['dwdm_edge', 'eth_edge', 'wireless_edge']
    range_end = 3

    def __init__(self, initial_value):
        super(Edgetype, self).__init__(initial_value)
