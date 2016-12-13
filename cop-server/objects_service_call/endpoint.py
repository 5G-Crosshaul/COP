from objects_common.jsonObject import JsonObject

class Endpoint(JsonObject):

    def __init__(self, json_struct=None):
        self.edgeEndId=""
        self.nodeId=""
        self.endpointId=""
        super(Endpoint, self).__init__(json_struct)

