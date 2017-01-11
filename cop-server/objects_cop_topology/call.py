from objects_common.jsonObject import JsonObject
from serviceEndpoint import ServiceEndpoint
from connection import Connection
from trafficParams import TrafficParams
from transportLayerType import TransportLayerType
from matchRules import MatchRules
from objects_common.keyedArrayType import KeyedArrayType
from objects_common.enumType import EnumType

class Call(JsonObject):

    def __init__(self, json_struct=None):
        self.contextId=""
        self.operStatus=Operstatus(0)
        self.callId=""
        self.zEnd=ServiceEndpoint() #import
        self.connections=KeyedArrayType(Connection, 'connectionId')
        self.trafficParams=TrafficParams() #import
        self.aEnd=ServiceEndpoint() #import
        self.transportLayer=TransportLayerType() #import
        self.match=MatchRules() #import
        super(Call, self).__init__(json_struct)

class Operstatus(EnumType):
    possible_values = ['down', 'up']
    range_end = 2

    def __init__(self, initial_value):
        super(Operstatus, self).__init__(initial_value)
