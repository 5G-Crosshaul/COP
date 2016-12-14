from objects_common.jsonObject import JsonObject
from objects_common.enumType import EnumType

class Label(JsonObject):

    def __init__(self, json_struct=None):
        self.labelType=Labeltype(0)
        self.labelValue=0
        super(Label, self).__init__(json_struct)

class Labeltype(EnumType):
    possible_values = ['GMPLS_FIXED', 'GMPLS_FLEXI']
    range_end = 2

    def __init__(self, initial_value):
        super(Labeltype, self).__init__(initial_value)
