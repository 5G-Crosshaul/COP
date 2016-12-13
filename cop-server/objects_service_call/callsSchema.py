from objects_common.jsonObject import JsonObject
from call import Call
from objects_common.keyedArrayType import KeyedArrayType

class CallsSchema(JsonObject):

    def __init__(self, json_struct=None):
        self.call=KeyedArrayType(Call, 'callId')
        super(CallsSchema, self).__init__(json_struct)

