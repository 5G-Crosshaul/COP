# Example, only works for COP
import json

from objects_common.keyedArrayType import KeyedArrayType
from objects_cop_call.callsSchema import CallsSchema as CallsSchema_object
from objects_cop_call.connectionsSchema import ConnectionsSchema as ConnectionsSchema_object
from objects_cop_topology.contextSchema import ContextSchema as ContextSchema_object

"""
class TopLevelObject(jsonObject):
    def __init__(self):
        self.calls = KeyedArrayType(Call, 'callId')
        self.connections = KeyedArrayType(Connection, 'connectionId')
        super(TopLevelObject, self).__init__()
"""

def json_dumps(js):
    # Pretty-print version of json.dumps
    return json.dumps(js, sort_keys=True, indent=4, separators=(',', ': '))


def byteify(input):
    # Convert JSON unicode strings to python byte strings, recursively on a json_struct
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

filename = 'server_backend_state.json'

calls = CallsSchema_object()
connections = ConnectionsSchema_object()
context = ContextSchema_object()

def save_state():
    json_struct = {}
    json_struct['calls'] = calls.json_serializer()
    json_struct['connections'] = connections.json_serializer()
    json_struct['context'] = context.json_serializer()

    json_string = json_dumps(json_struct)
    out = open(filename, 'w+')
    out.write(json_string)
    out.close()
    return True

def load_state():
    f = open(filename, 'rb')
    json_string = f.read()
    f.close()
    json_struct = byteify(json.loads(json_string))
    global calls
    calls = CallsSchema_object(json_struct['calls'])
    global connections
    connections = ConnectionsSchema_object(json_struct['connections'])
    global context
    context = ContextSchema_object(json_struct['context'])
    return True