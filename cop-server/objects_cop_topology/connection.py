from objects_common.jsonObject import JsonObject
from trafficParams import TrafficParams
from serviceEndpoint import ServiceEndpoint
from pathType import PathType
from transportLayerType import TransportLayerType
from matchRules import MatchRules
from objects_common.enumType import EnumType

class Connection(JsonObject):

    def __init__(self, json_struct=None):
        self.controllerDomainId=""
        self.contextId=""
        self.trafficParams=TrafficParams() #import
        self.connectionId=""
        self.zEnd=ServiceEndpoint() #import
        self.operStatus=Operstatus(0)
        self.aEnd=ServiceEndpoint() #import
        self.path=PathType() #import
        self.transportLayer=TransportLayerType() #import
        self.match=MatchRules() #import
        super(Connection, self).__init__(json_struct)

class Operstatus(EnumType):
    possible_values = ['down', 'up']
    range_end = 2

    def __init__(self, initial_value):
        super(Operstatus, self).__init__(initial_value)
