from objects_common.jsonObject import JsonObject
from trafficParams import TrafficParams
from endpoint import Endpoint
from pathType import PathType
from transportLayerType import TransportLayerType
from matchRules import MatchRules
from objects_common.enumType import EnumType

class Connection(JsonObject):

    def __init__(self, json_struct=None):
        self.controllerDomainId=""
        self.trafficParams=TrafficParams() #import
        self.connectionId=""
        self.zEnd=Endpoint() #import
        self.operStatus=Operstatus(0)
        self.aEnd=Endpoint() #import
        self.path=PathType() #import
        self.transportLayer=TransportLayerType() #import
        self.match=MatchRules() #import
        super(Connection, self).__init__(json_struct)

class Operstatus(EnumType):
    possible_values = ['down', 'up']
    range_end = 2

    def __init__(self, initial_value):
        super(Operstatus, self).__init__(initial_value)
