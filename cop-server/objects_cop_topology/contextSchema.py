from objects_common.jsonObject import JsonObject
from serviceEndpoint import ServiceEndpoint
from topology import Topology
from objects_common.keyedArrayType import KeyedArrayType

class ContextSchema(JsonObject):

    def __init__(self, json_struct=None):
        self.provider=False
        self.contextId=""
        self.parentContext=""
        self.serviceEndpoint=KeyedArrayType(ServiceEndpoint, 'endpointId')
        self.topology=KeyedArrayType(Topology, 'topologyId')
        super(ContextSchema, self).__init__(json_struct)

