from objects_common.jsonObject import JsonObject
from edgeEnd import EdgeEnd
from objects_common.arrayType import ArrayType
from objects_common.keyedArrayType import KeyedArrayType
from objects_common.enumType import EnumType

class Node(JsonObject):

    def __init__(self, json_struct=None):
        self.domain=""
        self.nodetype=Nodetype(0)
        self.underlayAbstractTopology=ArrayType.factory(str)
        self.edgeEnd=KeyedArrayType(EdgeEnd, 'edgeEndId')
        self.nodeId=""
        self.name=""
        super(Node, self).__init__(json_struct)

class Nodetype(EnumType):
    possible_values = ['OF', 'GMPLS', 'OF-W', 'ABSTRACT', 'OF-IOT', 'HOST']
    range_end = 6

    def __init__(self, initial_value):
        super(Nodetype, self).__init__(initial_value)
