from objects_common.jsonObject import JsonObject

class ServiceEndPointType(JsonObject):

    def __init__(self, json_struct=None):
        self.edgeEndId=""
        self.name=""
        self.sepId=""
        self.nodeId=""
        super(ServiceEndPointType, self).__init__(json_struct)

