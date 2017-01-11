from objects_common.jsonObject import JsonObject
from node import Node
from edge import Edge
from wirelessEdge import WirelessEdge
from ethEdge import EthEdge
from dwdmEdge import DwdmEdge
from objects_common.arrayType import ArrayType
from objects_common.keyedArrayType import KeyedArrayType

class Topology(JsonObject):

    def __init__(self, json_struct=None):
        self.topologyId=""
        self.underlayTopology=ArrayType.factory(str)
        self.nodes=KeyedArrayType(Node, 'nodeId')
        self.edges=KeyedArrayType((WirelessEdge,EthEdge,DwdmEdge), 'edgeId', 'edgeType')
        super(Topology, self).__init__(json_struct)

