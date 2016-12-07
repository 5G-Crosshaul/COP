from objects_common.jsonObject import JsonObject
from edgeEnd import EdgeEnd
from objects_common.arrayType import ArrayType
from objects_common.keyedArrayType import KeyedArrayType

class Node(JsonObject):

    def __init__(self, json_struct=None):
        self.edgeEnd=KeyedArrayType(EdgeEnd, 'edgeEndId')
        self.domain=""
        self.underlayAbstractTopology=ArrayType.factory(str)
        self.nodeId=""
        self.name=""
        super(Node, self).__init__(json_struct)

