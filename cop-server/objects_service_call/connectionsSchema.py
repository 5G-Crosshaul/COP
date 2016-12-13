from objects_common.jsonObject import JsonObject
from connection import Connection
from objects_common.keyedArrayType import KeyedArrayType

class ConnectionsSchema(JsonObject):

    def __init__(self, json_struct=None):
        self.connection=KeyedArrayType(Connection, 'connectionId')
        super(ConnectionsSchema, self).__init__(json_struct)

