from objects_common.jsonObject import JsonObject

class ServiceEndpoint(JsonObject):

    def __init__(self, json_struct=None):
        self.edgeEndId=""
        self.name=""
        self.endpointId=""
        self.nodeId=""
        super(ServiceEndpoint, self).__init__(json_struct)

