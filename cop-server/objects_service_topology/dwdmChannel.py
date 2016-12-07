from objects_common.jsonObject import JsonObject

class DwdmChannel(JsonObject):

    def __init__(self, json_struct=None):
        self.state=0
        self.g694Id=0
        super(DwdmChannel, self).__init__(json_struct)

