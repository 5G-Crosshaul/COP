from objects_common.jsonObject import JsonObject
from serviceEndpoint import ServiceEndpoint
from label import Label
from objects_common.keyedArrayType import KeyedArrayType

class PathType(JsonObject):

    def __init__(self, json_struct=None):
        self.multiLayer=False
        self.topoComponents=KeyedArrayType(ServiceEndpoint, 'endpointId')
        self.id=""
        self.noPath=False
        self.label=Label() #import
        super(PathType, self).__init__(json_struct)

