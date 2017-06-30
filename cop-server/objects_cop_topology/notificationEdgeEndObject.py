from objects_common.jsonObject import JsonObject
from edgeEnd import EdgeEnd

class NotificationEdgeEndObject(JsonObject):

    def __init__(self, json_struct=None):
        self.edgeEnd=EdgeEnd() #import
        self.nodeId=""
        super(NotificationEdgeEndObject, self).__init__(json_struct)

