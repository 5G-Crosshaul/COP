from objects_common.jsonObject import JsonObject

class TransportLayerType(JsonObject):

    def __init__(self, json_struct=None):
        self.action=""
        self.layer=""
        self.direction=""
        self.layerId=""
        super(TransportLayerType, self).__init__(json_struct)

