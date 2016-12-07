from objects_common.jsonObject import JsonObject
from objects_common.arrayType import ArrayType

class Bitmap(JsonObject):

    def __init__(self, json_struct=None):
        self.arrayBits=ArrayType.factory(int)
        self.numChannels=0
        super(Bitmap, self).__init__(json_struct)

