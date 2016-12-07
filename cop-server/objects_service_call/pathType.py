from objects_common.jsonObject import JsonObject
from endpoint import Endpoint
from label import Label
from objects_common.keyedArrayType import KeyedArrayType

class PathType(JsonObject):

    def __init__(self, json_struct=None):
        self.multiLayer=False
        self.topoComponents=KeyedArrayType(Endpoint, 'endpointId')
        self.id=""
        self.noPath=False
        self.label=Label() #import
        super(PathType, self).__init__(json_struct)

