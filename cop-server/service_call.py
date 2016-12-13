from flask import json, Blueprint, request, Response
from flask.views import MethodView
import sys
from objects_common.keyedArrayType import KeyedArrayKeyError

import base64
import re

# BACKEND FUNCTIONS
from funcs_service_call.connectionsConnectionImpl import ConnectionsConnectionImpl
from funcs_service_call.callsCallCallidConnectionsConnectionidMatchInclude_PathLabelImpl import CallsCallCallidConnectionsConnectionidMatchInclude_PathLabelImpl
from funcs_service_call.callsCallCallidTraffic_ParamsImpl import CallsCallCallidTraffic_ParamsImpl
from funcs_service_call.callsCallCallidConnectionsConnectionidMatchImpl import CallsCallCallidConnectionsConnectionidMatchImpl
from funcs_service_call.connectionsConnectionConnectionidTraffic_ParamsImpl import ConnectionsConnectionConnectionidTraffic_ParamsImpl
from funcs_service_call.callsCallCallidConnectionsConnectionidMatchInclude_PathTopo_ComponentsImpl import CallsCallCallidConnectionsConnectionidMatchInclude_PathTopo_ComponentsImpl
from funcs_service_call.callsCallCallidConnectionsConnectionidTraffic_ParamsImpl import CallsCallCallidConnectionsConnectionidTraffic_ParamsImpl
from funcs_service_call.callsCallCallidConnectionsConnectionidPathTopo_ComponentsEndpointidImpl import CallsCallCallidConnectionsConnectionidPathTopo_ComponentsEndpointidImpl
from funcs_service_call.callsCallCallidConnectionsConnectionidMatchInclude_PathImpl import CallsCallCallidConnectionsConnectionidMatchInclude_PathImpl
from funcs_service_call.callsCallCallidConnectionsConnectionidZendImpl import CallsCallCallidConnectionsConnectionidZendImpl
from funcs_service_call.connectionsConnectionConnectionidAendImpl import ConnectionsConnectionConnectionidAendImpl
from funcs_service_call.callsCallCallidTransport_LayerImpl import CallsCallCallidTransport_LayerImpl
from funcs_service_call.connectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsEndpointidImpl import ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsEndpointidImpl
from funcs_service_call.callsCallCallidConnectionsConnectionidImpl import CallsCallCallidConnectionsConnectionidImpl
from funcs_service_call.callsImpl import CallsImpl
from funcs_service_call.callsCallCallidMatchInclude_PathTopo_ComponentsEndpointidImpl import CallsCallCallidMatchInclude_PathTopo_ComponentsEndpointidImpl
from funcs_service_call.connectionsConnectionConnectionidMatchInclude_PathLabelImpl import ConnectionsConnectionConnectionidMatchInclude_PathLabelImpl
from funcs_service_call.connectionsConnectionConnectionidTransport_LayerImpl import ConnectionsConnectionConnectionidTransport_LayerImpl
from funcs_service_call.connectionsConnectionConnectionidImpl import ConnectionsConnectionConnectionidImpl
from funcs_service_call.callsCallCallidConnectionsConnectionidPathLabelImpl import CallsCallCallidConnectionsConnectionidPathLabelImpl
from funcs_service_call.connectionsConnectionConnectionidPathImpl import ConnectionsConnectionConnectionidPathImpl
from funcs_service_call.callsCallCallidMatchInclude_PathTopo_ComponentsImpl import CallsCallCallidMatchInclude_PathTopo_ComponentsImpl
from funcs_service_call.callsCallCallidMatchImpl import CallsCallCallidMatchImpl
from funcs_service_call.callsCallCallidConnectionsImpl import CallsCallCallidConnectionsImpl
from funcs_service_call.callsCallCallidConnectionsConnectionidMatchInclude_PathTopo_ComponentsEndpointidImpl import CallsCallCallidConnectionsConnectionidMatchInclude_PathTopo_ComponentsEndpointidImpl
from funcs_service_call.callsCallCallidConnectionsConnectionidPathTopo_ComponentsImpl import CallsCallCallidConnectionsConnectionidPathTopo_ComponentsImpl
from funcs_service_call.callsCallCallidConnectionsConnectionidAendImpl import CallsCallCallidConnectionsConnectionidAendImpl
from funcs_service_call.connectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsImpl import ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsImpl
from funcs_service_call.callsCallCallidConnectionsConnectionidPathImpl import CallsCallCallidConnectionsConnectionidPathImpl
from funcs_service_call.callsCallCallidImpl import CallsCallCallidImpl
from funcs_service_call.connectionsConnectionConnectionidZendImpl import ConnectionsConnectionConnectionidZendImpl
from funcs_service_call.connectionsConnectionConnectionidPathTopo_ComponentsImpl import ConnectionsConnectionConnectionidPathTopo_ComponentsImpl
from funcs_service_call.callsCallImpl import CallsCallImpl
from funcs_service_call.connectionsImpl import ConnectionsImpl
from funcs_service_call.connectionsConnectionConnectionidPathLabelImpl import ConnectionsConnectionConnectionidPathLabelImpl
from funcs_service_call.connectionsConnectionConnectionidMatchImpl import ConnectionsConnectionConnectionidMatchImpl
from funcs_service_call.callsCallCallidConnectionsConnectionidTransport_LayerImpl import CallsCallCallidConnectionsConnectionidTransport_LayerImpl
from funcs_service_call.connectionsConnectionConnectionidMatchInclude_PathImpl import ConnectionsConnectionConnectionidMatchInclude_PathImpl
from funcs_service_call.callsCallCallidMatchInclude_PathImpl import CallsCallCallidMatchInclude_PathImpl
from funcs_service_call.connectionsConnectionConnectionidPathTopo_ComponentsEndpointidImpl import ConnectionsConnectionConnectionidPathTopo_ComponentsEndpointidImpl
from funcs_service_call.callsCallCallidAendImpl import CallsCallCallidAendImpl
from funcs_service_call.callsCallCallidMatchInclude_PathLabelImpl import CallsCallCallidMatchInclude_PathLabelImpl
from funcs_service_call.callsCallCallidZendImpl import CallsCallCallidZendImpl

# CALLABLE OBJECTS
from objects_service_call.endpoint import Endpoint
from objects_service_call.connectionsSchema import ConnectionsSchema
from objects_service_call.trafficParams import TrafficParams
from objects_service_call.pathType import PathType
from objects_service_call.label import Label
from objects_service_call.transportLayerType import TransportLayerType
from objects_service_call.connection import Connection
from objects_service_call.call import Call
from objects_service_call.callsSchema import CallsSchema
from objects_service_call.matchRules import MatchRules

users = {"admin": "pswd1", "user": "pswd2"}

setattr(sys.modules[__name__], __name__,  Blueprint(__name__, __name__))



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

def json_loads(json_string):
    # Try to use json.loads and raise HTTP Error
    try:
        json_struct = json.loads(json_string) #json parser.
    except ValueError:
        raise BadRequestError("Malformed JSON")
    else:
        return byteify(json_struct)

def json_dumps(js):
    # Pretty-print version of json.dumps
    return json.dumps(js, sort_keys=True, indent=4, separators=(',', ': '))

def create_instance(klass, json_struct, id=None):
    # Try to create an object instance and raise HTTP Errors
    try:
        new_object = klass(json_struct) # Creates an object instance of type klass from the json_struct data
    except KeyError as inst:
        return BadRequestError("Unknown entity name in JSON:" + "<br>" + inst.args[0])
    except TypeError as inst:
        key = inst.args[0]
        value = json.dumps(inst.args[1])
        return BadRequestError("Incorrect type in JSON:" + "<br>" +
                              key + " was:" + "<br>" +
                              value + "<br>" +
                              "Allowed type:" + "<br>" +
                              inst.args[2])
    except ValueError as inst:
        if type(inst.args[1]) == str:
            return BadRequestError("Incorrect value in JSON:" + "<br>" +
                                  "Enum " + inst.args[0] + " was:" + "<br>" +
                                  inst.args[1] + "<br>" +
                                  "Allowed values:" + "<br>" +
                                  "[" + ", ".join(inst.args[2]) + "]")
        elif type(inst.args[1]) == int:
            return BadRequestError("Incorrect value in JSON:" + "<br>" +
                                  "Enum " + inst.args[0] + " was:" + "<br>" +
                                  str(inst.args[1]) + "<br>" +
                                  "Allowed range:" + "<br>" +
                                  "1 - " + str(inst.args[2]))
    except KeyedArrayKeyError as inst:
        return BadRequestError("Error in JSON:" + "<br>" +
                              "Missing key in list:" + "<br>" +
                              inst.args[0] + "<br>" +
                              "Received JSON:" + "<br>" +
                              json.dumps(inst.args[1]) + "<br>" +
                              "Key name:" + "<br>" +
                              inst.args[2])
    else:
        # Check if the id given in the URL matches the id given in the body
        if id != None and id[0] != getattr(new_object, id[1]):
            return BadRequestError(id[1] + " in body not matching " + id[1] + " in URL")
        else:
            return new_object

def modify_instance(existing_object, json_struct):
    try:
        existing_object.load_json(json_struct)
    except KeyError as inst:
        return BadRequestError("Unknown entity name in JSON:" + "<br>" + inst.args[0])
    except TypeError as inst:
        key = inst.args[0]
        value = json.dumps(inst.args[1])
        return BadRequestError("Incorrect type in JSON:" + "<br>" +
                              key + " was:" + "<br>" +
                              value + "<br>" +
                              "Allowed type:" + "<br>" +
                              inst.args[2])
    except ValueError as inst:
        if type(inst.args[1]) == str:
            return BadRequestError("Incorrect value in JSON:" + "<br>" +
                                  "Enum " + inst.args[0] + " was:" + "<br>" +
                                  inst.args[1] + "<br>" +
                                  "Allowed values:" + "<br>" +
                                  "[" + ", ".join(inst.args[2]) + "]")
        elif type(inst.args[1]) == int:
            return BadRequestError("Incorrect value in JSON:" + "<br>" +
                                  "Enum " + inst.args[0] + " was:" + "<br>" +
                                  str(inst.args[1]) + "<br>" +
                                  "Allowed range:" + "<br>" +
                                  "1 - " + str(inst.args[2]))
    except KeyedArrayKeyError as inst:
        return BadRequestError("Error in JSON:" + "<br>" +
                              "Missing key in list:" + "<br>" +
                              inst.args[0] + "<br>" +
                              "Received JSON:" + "<br>" +
                              json.dumps(inst.args[1]) + "<br>" +
                              "Key name:" + "<br>" +
                              inst.args[2])
    else:
        return existing_object


class NotFoundError(Response):
    def __init__(self, message):
        super(NotFoundError, self).__init__()
        self.status = '404 '+message
        self.status_code = 404
        self.headers = {'Content-Type': 'text/html'}
        self.data = '<h1>'+message+'</h1>'

class BadRequestError(Response):
    def __init__(self, message):
        super(BadRequestError, self).__init__()
        self.status = '400 '+message
        self.status_code = 400
        self.headers = {'Content-Type': 'text/html'}
        self.data = '<h1>'+message+'</h1>'

class Unauthorized(Response):
    def __init__(self, message):
        super(Unauthorized, self).__init__()
        self.status = '401 '+message
        self.status_code = 401
        self.headers = {'WWW-Authenticate','Basic realm="Auth example"'}
        self.data = '<h1>'+message+'</h1>'

class Successful(Response):
    def __init__(self, message, info=''):
        super(Successful, self).__init__()
        self.status = '200 '+message
        self.status_code = 200
        self.headers = {'Content-Type': 'application/json'}
        self.data = info


#/restconf/config/connections/connection/
class ConnectionsConnectionMethodView(MethodView):

    def get(self, ):
        print "Retrieve operation of resource: connection"
        try:
            response = ConnectionsConnectionImpl.get()
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/(\w+)/match/include_path/label/
class CallsCallCallidConnectionsConnectionidMatchInclude_PathLabelMethodView(MethodView):

    def get(self, callId, connectionId):
        print "Retrieve operation of resource: label"
        try:
            response = CallsCallCallidConnectionsConnectionidMatchInclude_PathLabelImpl.get(callId, connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/traffic_params/
class CallsCallCallidTraffic_ParamsMethodView(MethodView):

    def put(self, callId):
        print "Update operation of resource: traffic_params"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = CallsCallCallidTraffic_ParamsImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(TrafficParams, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidTraffic_ParamsImpl.put(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    CallsCallCallidTraffic_ParamsImpl.put(callId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, callId):
        print "Create operation of resource: traffic_params"
        try:
            response = CallsCallCallidTraffic_ParamsImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(TrafficParams, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidTraffic_ParamsImpl.post(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, callId):
        print "Delete operation of resource: traffic_params"
        try:
            response=CallsCallCallidTraffic_ParamsImpl.delete(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, callId):
        print "Retrieve operation of resource: traffic_params"
        try:
            response = CallsCallCallidTraffic_ParamsImpl.get(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/(\w+)/match/
class CallsCallCallidConnectionsConnectionidMatchMethodView(MethodView):

    def get(self, callId, connectionId):
        print "Retrieve operation of resource: match"
        try:
            response = CallsCallCallidConnectionsConnectionidMatchImpl.get(callId, connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/connection/(\w+)/traffic_params/
class ConnectionsConnectionConnectionidTraffic_ParamsMethodView(MethodView):

    def put(self, connectionId):
        print "Update operation of resource: traffic_params"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = ConnectionsConnectionConnectionidTraffic_ParamsImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(TrafficParams, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidTraffic_ParamsImpl.put(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    ConnectionsConnectionConnectionidTraffic_ParamsImpl.put(connectionId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, connectionId):
        print "Create operation of resource: traffic_params"
        try:
            response = ConnectionsConnectionConnectionidTraffic_ParamsImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(TrafficParams, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidTraffic_ParamsImpl.post(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, connectionId):
        print "Delete operation of resource: traffic_params"
        try:
            response=ConnectionsConnectionConnectionidTraffic_ParamsImpl.delete(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, connectionId):
        print "Retrieve operation of resource: traffic_params"
        try:
            response = ConnectionsConnectionConnectionidTraffic_ParamsImpl.get(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/(\w+)/match/include_path/topo_components/
class CallsCallCallidConnectionsConnectionidMatchInclude_PathTopo_ComponentsMethodView(MethodView):

    def get(self, callId, connectionId):
        print "Retrieve operation of resource: topo_components"
        try:
            response = CallsCallCallidConnectionsConnectionidMatchInclude_PathTopo_ComponentsImpl.get(callId, connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/(\w+)/traffic_params/
class CallsCallCallidConnectionsConnectionidTraffic_ParamsMethodView(MethodView):

    def get(self, callId, connectionId):
        print "Retrieve operation of resource: traffic_params"
        try:
            response = CallsCallCallidConnectionsConnectionidTraffic_ParamsImpl.get(callId, connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/(\w+)/path/topo_components/(\w+)/
class CallsCallCallidConnectionsConnectionidPathTopo_ComponentsEndpointidMethodView(MethodView):

    def get(self, callId, connectionId, endpointId):
        print "Retrieve operation of resource: topo_components"
        try:
            response = CallsCallCallidConnectionsConnectionidPathTopo_ComponentsEndpointidImpl.get(callId, connectionId, endpointId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/(\w+)/match/include_path/
class CallsCallCallidConnectionsConnectionidMatchInclude_PathMethodView(MethodView):

    def get(self, callId, connectionId):
        print "Retrieve operation of resource: include_path"
        try:
            response = CallsCallCallidConnectionsConnectionidMatchInclude_PathImpl.get(callId, connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/(\w+)/zEnd/
class CallsCallCallidConnectionsConnectionidZendMethodView(MethodView):

    def get(self, callId, connectionId):
        print "Retrieve operation of resource: zEnd"
        try:
            response = CallsCallCallidConnectionsConnectionidZendImpl.get(callId, connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/connection/(\w+)/aEnd/
class ConnectionsConnectionConnectionidAendMethodView(MethodView):

    def put(self, connectionId):
        print "Update operation of resource: aEnd"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = ConnectionsConnectionConnectionidAendImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(Endpoint, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidAendImpl.put(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    ConnectionsConnectionConnectionidAendImpl.put(connectionId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, connectionId):
        print "Create operation of resource: aEnd"
        try:
            response = ConnectionsConnectionConnectionidAendImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(Endpoint, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidAendImpl.post(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, connectionId):
        print "Delete operation of resource: aEnd"
        try:
            response=ConnectionsConnectionConnectionidAendImpl.delete(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, connectionId):
        print "Retrieve operation of resource: aEnd"
        try:
            response = ConnectionsConnectionConnectionidAendImpl.get(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/transport_layer/
class CallsCallCallidTransport_LayerMethodView(MethodView):

    def put(self, callId):
        print "Update operation of resource: transport_layer"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = CallsCallCallidTransport_LayerImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(TransportLayerType, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidTransport_LayerImpl.put(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    CallsCallCallidTransport_LayerImpl.put(callId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, callId):
        print "Create operation of resource: transport_layer"
        try:
            response = CallsCallCallidTransport_LayerImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(TransportLayerType, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidTransport_LayerImpl.post(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, callId):
        print "Delete operation of resource: transport_layer"
        try:
            response=CallsCallCallidTransport_LayerImpl.delete(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, callId):
        print "Retrieve operation of resource: transport_layer"
        try:
            response = CallsCallCallidTransport_LayerImpl.get(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/connection/(\w+)/match/include_path/topo_components/(\w+)/
class ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsEndpointidMethodView(MethodView):

    def put(self, connectionId, endpointId):
        print "Update operation of resource: topo_components"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsEndpointidImpl.get(connectionId, endpointId)
        except KeyError as inst:
            if inst.args[0] != 'endpointId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(Endpoint, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsEndpointidImpl.put(connectionId, endpointId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsEndpointidImpl.put(connectionId, endpointId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, connectionId, endpointId):
        print "Create operation of resource: topo_components"
        try:
            response = ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsEndpointidImpl.get(connectionId, endpointId)
        except KeyError as inst:
            if inst.args[0] != 'endpointId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(Endpoint, json_struct, (endpointId,'endpointId'))
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsEndpointidImpl.post(connectionId, endpointId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, connectionId, endpointId):
        print "Delete operation of resource: topo_components"
        try:
            response=ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsEndpointidImpl.delete(connectionId, endpointId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, connectionId, endpointId):
        print "Retrieve operation of resource: topo_components"
        try:
            response = ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsEndpointidImpl.get(connectionId, endpointId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/(\w+)/
class CallsCallCallidConnectionsConnectionidMethodView(MethodView):

    def get(self, callId, connectionId):
        print "Retrieve operation of resource: connections"
        try:
            response = CallsCallCallidConnectionsConnectionidImpl.get(callId, connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/
class CallsMethodView(MethodView):

    def put(self, ):
        print "Update operation of resource: calls"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = CallsImpl.get()
        except KeyError as inst:
            if inst.args[0] != '':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(CallsSchema, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsImpl.put(new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    CallsImpl.put(existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, ):
        print "Create operation of resource: calls"
        try:
            response = CallsImpl.get()
        except KeyError as inst:
            if inst.args[0] != '':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(CallsSchema, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsImpl.post(new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, ):
        print "Delete operation of resource: calls"
        try:
            response=CallsImpl.delete()
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, ):
        print "Retrieve operation of resource: calls"
        try:
            response = CallsImpl.get()
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/match/include_path/topo_components/(\w+)/
class CallsCallCallidMatchInclude_PathTopo_ComponentsEndpointidMethodView(MethodView):

    def put(self, callId, endpointId):
        print "Update operation of resource: topo_components"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = CallsCallCallidMatchInclude_PathTopo_ComponentsEndpointidImpl.get(callId, endpointId)
        except KeyError as inst:
            if inst.args[0] != 'endpointId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(Endpoint, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidMatchInclude_PathTopo_ComponentsEndpointidImpl.put(callId, endpointId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    CallsCallCallidMatchInclude_PathTopo_ComponentsEndpointidImpl.put(callId, endpointId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, callId, endpointId):
        print "Create operation of resource: topo_components"
        try:
            response = CallsCallCallidMatchInclude_PathTopo_ComponentsEndpointidImpl.get(callId, endpointId)
        except KeyError as inst:
            if inst.args[0] != 'endpointId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(Endpoint, json_struct, (endpointId,'endpointId'))
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidMatchInclude_PathTopo_ComponentsEndpointidImpl.post(callId, endpointId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, callId, endpointId):
        print "Delete operation of resource: topo_components"
        try:
            response=CallsCallCallidMatchInclude_PathTopo_ComponentsEndpointidImpl.delete(callId, endpointId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, callId, endpointId):
        print "Retrieve operation of resource: topo_components"
        try:
            response = CallsCallCallidMatchInclude_PathTopo_ComponentsEndpointidImpl.get(callId, endpointId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/connection/(\w+)/match/include_path/label/
class ConnectionsConnectionConnectionidMatchInclude_PathLabelMethodView(MethodView):

    def put(self, connectionId):
        print "Update operation of resource: label"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = ConnectionsConnectionConnectionidMatchInclude_PathLabelImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(Label, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidMatchInclude_PathLabelImpl.put(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    ConnectionsConnectionConnectionidMatchInclude_PathLabelImpl.put(connectionId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, connectionId):
        print "Create operation of resource: label"
        try:
            response = ConnectionsConnectionConnectionidMatchInclude_PathLabelImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(Label, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidMatchInclude_PathLabelImpl.post(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, connectionId):
        print "Delete operation of resource: label"
        try:
            response=ConnectionsConnectionConnectionidMatchInclude_PathLabelImpl.delete(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, connectionId):
        print "Retrieve operation of resource: label"
        try:
            response = ConnectionsConnectionConnectionidMatchInclude_PathLabelImpl.get(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/connection/(\w+)/transport_layer/
class ConnectionsConnectionConnectionidTransport_LayerMethodView(MethodView):

    def put(self, connectionId):
        print "Update operation of resource: transport_layer"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = ConnectionsConnectionConnectionidTransport_LayerImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(TransportLayerType, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidTransport_LayerImpl.put(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    ConnectionsConnectionConnectionidTransport_LayerImpl.put(connectionId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, connectionId):
        print "Create operation of resource: transport_layer"
        try:
            response = ConnectionsConnectionConnectionidTransport_LayerImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(TransportLayerType, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidTransport_LayerImpl.post(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, connectionId):
        print "Delete operation of resource: transport_layer"
        try:
            response=ConnectionsConnectionConnectionidTransport_LayerImpl.delete(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, connectionId):
        print "Retrieve operation of resource: transport_layer"
        try:
            response = ConnectionsConnectionConnectionidTransport_LayerImpl.get(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/connection/(\w+)/
class ConnectionsConnectionConnectionidMethodView(MethodView):

    def put(self, connectionId):
        print "Update operation of resource: connection"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = ConnectionsConnectionConnectionidImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(Connection, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidImpl.put(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    ConnectionsConnectionConnectionidImpl.put(connectionId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, connectionId):
        print "Create operation of resource: connection"
        try:
            response = ConnectionsConnectionConnectionidImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(Connection, json_struct, (connectionId,'connectionId'))
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidImpl.post(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, connectionId):
        print "Delete operation of resource: connection"
        try:
            response=ConnectionsConnectionConnectionidImpl.delete(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, connectionId):
        print "Retrieve operation of resource: connection"
        try:
            response = ConnectionsConnectionConnectionidImpl.get(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/(\w+)/path/label/
class CallsCallCallidConnectionsConnectionidPathLabelMethodView(MethodView):

    def get(self, callId, connectionId):
        print "Retrieve operation of resource: label"
        try:
            response = CallsCallCallidConnectionsConnectionidPathLabelImpl.get(callId, connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/connection/(\w+)/path/
class ConnectionsConnectionConnectionidPathMethodView(MethodView):

    def put(self, connectionId):
        print "Update operation of resource: path"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = ConnectionsConnectionConnectionidPathImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(PathType, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidPathImpl.put(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    ConnectionsConnectionConnectionidPathImpl.put(connectionId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, connectionId):
        print "Create operation of resource: path"
        try:
            response = ConnectionsConnectionConnectionidPathImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(PathType, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidPathImpl.post(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, connectionId):
        print "Delete operation of resource: path"
        try:
            response=ConnectionsConnectionConnectionidPathImpl.delete(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, connectionId):
        print "Retrieve operation of resource: path"
        try:
            response = ConnectionsConnectionConnectionidPathImpl.get(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/match/include_path/topo_components/
class CallsCallCallidMatchInclude_PathTopo_ComponentsMethodView(MethodView):

    def get(self, callId):
        print "Retrieve operation of resource: topo_components"
        try:
            response = CallsCallCallidMatchInclude_PathTopo_ComponentsImpl.get(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/match/
class CallsCallCallidMatchMethodView(MethodView):

    def put(self, callId):
        print "Update operation of resource: match"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = CallsCallCallidMatchImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(MatchRules, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidMatchImpl.put(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    CallsCallCallidMatchImpl.put(callId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, callId):
        print "Create operation of resource: match"
        try:
            response = CallsCallCallidMatchImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(MatchRules, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidMatchImpl.post(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, callId):
        print "Delete operation of resource: match"
        try:
            response=CallsCallCallidMatchImpl.delete(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, callId):
        print "Retrieve operation of resource: match"
        try:
            response = CallsCallCallidMatchImpl.get(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/
class CallsCallCallidConnectionsMethodView(MethodView):

    def get(self, callId):
        print "Retrieve operation of resource: connections"
        try:
            response = CallsCallCallidConnectionsImpl.get(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/(\w+)/match/include_path/topo_components/(\w+)/
class CallsCallCallidConnectionsConnectionidMatchInclude_PathTopo_ComponentsEndpointidMethodView(MethodView):

    def get(self, callId, connectionId, endpointId):
        print "Retrieve operation of resource: topo_components"
        try:
            response = CallsCallCallidConnectionsConnectionidMatchInclude_PathTopo_ComponentsEndpointidImpl.get(callId, connectionId, endpointId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/(\w+)/path/topo_components/
class CallsCallCallidConnectionsConnectionidPathTopo_ComponentsMethodView(MethodView):

    def get(self, callId, connectionId):
        print "Retrieve operation of resource: topo_components"
        try:
            response = CallsCallCallidConnectionsConnectionidPathTopo_ComponentsImpl.get(callId, connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/(\w+)/aEnd/
class CallsCallCallidConnectionsConnectionidAendMethodView(MethodView):

    def get(self, callId, connectionId):
        print "Retrieve operation of resource: aEnd"
        try:
            response = CallsCallCallidConnectionsConnectionidAendImpl.get(callId, connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/connection/(\w+)/match/include_path/topo_components/
class ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsMethodView(MethodView):

    def get(self, connectionId):
        print "Retrieve operation of resource: topo_components"
        try:
            response = ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsImpl.get(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/(\w+)/path/
class CallsCallCallidConnectionsConnectionidPathMethodView(MethodView):

    def get(self, callId, connectionId):
        print "Retrieve operation of resource: path"
        try:
            response = CallsCallCallidConnectionsConnectionidPathImpl.get(callId, connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/
class CallsCallCallidMethodView(MethodView):

    def put(self, callId):
        print "Update operation of resource: call"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = CallsCallCallidImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(Call, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidImpl.put(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    CallsCallCallidImpl.put(callId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, callId):
        print "Create operation of resource: call"
        try:
            response = CallsCallCallidImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(Call, json_struct, (callId,'callId'))
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidImpl.post(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, callId):
        print "Delete operation of resource: call"
        try:
            response=CallsCallCallidImpl.delete(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, callId):
        print "Retrieve operation of resource: call"
        try:
            response = CallsCallCallidImpl.get(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/connection/(\w+)/zEnd/
class ConnectionsConnectionConnectionidZendMethodView(MethodView):

    def put(self, connectionId):
        print "Update operation of resource: zEnd"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = ConnectionsConnectionConnectionidZendImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(Endpoint, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidZendImpl.put(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    ConnectionsConnectionConnectionidZendImpl.put(connectionId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, connectionId):
        print "Create operation of resource: zEnd"
        try:
            response = ConnectionsConnectionConnectionidZendImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(Endpoint, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidZendImpl.post(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, connectionId):
        print "Delete operation of resource: zEnd"
        try:
            response=ConnectionsConnectionConnectionidZendImpl.delete(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, connectionId):
        print "Retrieve operation of resource: zEnd"
        try:
            response = ConnectionsConnectionConnectionidZendImpl.get(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/connection/(\w+)/path/topo_components/
class ConnectionsConnectionConnectionidPathTopo_ComponentsMethodView(MethodView):

    def get(self, connectionId):
        print "Retrieve operation of resource: topo_components"
        try:
            response = ConnectionsConnectionConnectionidPathTopo_ComponentsImpl.get(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/
class CallsCallMethodView(MethodView):

    def get(self, ):
        print "Retrieve operation of resource: call"
        try:
            response = CallsCallImpl.get()
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/
class ConnectionsMethodView(MethodView):

    def put(self, ):
        print "Update operation of resource: connections"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = ConnectionsImpl.get()
        except KeyError as inst:
            if inst.args[0] != '':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(ConnectionsSchema, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsImpl.put(new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    ConnectionsImpl.put(existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, ):
        print "Create operation of resource: connections"
        try:
            response = ConnectionsImpl.get()
        except KeyError as inst:
            if inst.args[0] != '':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(ConnectionsSchema, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsImpl.post(new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, ):
        print "Delete operation of resource: connections"
        try:
            response=ConnectionsImpl.delete()
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, ):
        print "Retrieve operation of resource: connections"
        try:
            response = ConnectionsImpl.get()
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/connection/(\w+)/path/label/
class ConnectionsConnectionConnectionidPathLabelMethodView(MethodView):

    def put(self, connectionId):
        print "Update operation of resource: label"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = ConnectionsConnectionConnectionidPathLabelImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(Label, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidPathLabelImpl.put(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    ConnectionsConnectionConnectionidPathLabelImpl.put(connectionId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, connectionId):
        print "Create operation of resource: label"
        try:
            response = ConnectionsConnectionConnectionidPathLabelImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(Label, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidPathLabelImpl.post(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, connectionId):
        print "Delete operation of resource: label"
        try:
            response=ConnectionsConnectionConnectionidPathLabelImpl.delete(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, connectionId):
        print "Retrieve operation of resource: label"
        try:
            response = ConnectionsConnectionConnectionidPathLabelImpl.get(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/connection/(\w+)/match/
class ConnectionsConnectionConnectionidMatchMethodView(MethodView):

    def put(self, connectionId):
        print "Update operation of resource: match"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = ConnectionsConnectionConnectionidMatchImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(MatchRules, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidMatchImpl.put(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    ConnectionsConnectionConnectionidMatchImpl.put(connectionId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, connectionId):
        print "Create operation of resource: match"
        try:
            response = ConnectionsConnectionConnectionidMatchImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(MatchRules, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidMatchImpl.post(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, connectionId):
        print "Delete operation of resource: match"
        try:
            response=ConnectionsConnectionConnectionidMatchImpl.delete(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, connectionId):
        print "Retrieve operation of resource: match"
        try:
            response = ConnectionsConnectionConnectionidMatchImpl.get(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/connections/(\w+)/transport_layer/
class CallsCallCallidConnectionsConnectionidTransport_LayerMethodView(MethodView):

    def get(self, callId, connectionId):
        print "Retrieve operation of resource: transport_layer"
        try:
            response = CallsCallCallidConnectionsConnectionidTransport_LayerImpl.get(callId, connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/connection/(\w+)/match/include_path/
class ConnectionsConnectionConnectionidMatchInclude_PathMethodView(MethodView):

    def put(self, connectionId):
        print "Update operation of resource: include_path"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = ConnectionsConnectionConnectionidMatchInclude_PathImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(PathType, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidMatchInclude_PathImpl.put(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    ConnectionsConnectionConnectionidMatchInclude_PathImpl.put(connectionId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, connectionId):
        print "Create operation of resource: include_path"
        try:
            response = ConnectionsConnectionConnectionidMatchInclude_PathImpl.get(connectionId)
        except KeyError as inst:
            if inst.args[0] != 'connectionId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(PathType, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidMatchInclude_PathImpl.post(connectionId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, connectionId):
        print "Delete operation of resource: include_path"
        try:
            response=ConnectionsConnectionConnectionidMatchInclude_PathImpl.delete(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, connectionId):
        print "Retrieve operation of resource: include_path"
        try:
            response = ConnectionsConnectionConnectionidMatchInclude_PathImpl.get(connectionId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/match/include_path/
class CallsCallCallidMatchInclude_PathMethodView(MethodView):

    def put(self, callId):
        print "Update operation of resource: include_path"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = CallsCallCallidMatchInclude_PathImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(PathType, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidMatchInclude_PathImpl.put(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    CallsCallCallidMatchInclude_PathImpl.put(callId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, callId):
        print "Create operation of resource: include_path"
        try:
            response = CallsCallCallidMatchInclude_PathImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(PathType, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidMatchInclude_PathImpl.post(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, callId):
        print "Delete operation of resource: include_path"
        try:
            response=CallsCallCallidMatchInclude_PathImpl.delete(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, callId):
        print "Retrieve operation of resource: include_path"
        try:
            response = CallsCallCallidMatchInclude_PathImpl.get(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/connections/connection/(\w+)/path/topo_components/(\w+)/
class ConnectionsConnectionConnectionidPathTopo_ComponentsEndpointidMethodView(MethodView):

    def put(self, connectionId, endpointId):
        print "Update operation of resource: topo_components"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = ConnectionsConnectionConnectionidPathTopo_ComponentsEndpointidImpl.get(connectionId, endpointId)
        except KeyError as inst:
            if inst.args[0] != 'endpointId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(Endpoint, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidPathTopo_ComponentsEndpointidImpl.put(connectionId, endpointId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    ConnectionsConnectionConnectionidPathTopo_ComponentsEndpointidImpl.put(connectionId, endpointId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, connectionId, endpointId):
        print "Create operation of resource: topo_components"
        try:
            response = ConnectionsConnectionConnectionidPathTopo_ComponentsEndpointidImpl.get(connectionId, endpointId)
        except KeyError as inst:
            if inst.args[0] != 'endpointId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(Endpoint, json_struct, (endpointId,'endpointId'))
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    ConnectionsConnectionConnectionidPathTopo_ComponentsEndpointidImpl.post(connectionId, endpointId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, connectionId, endpointId):
        print "Delete operation of resource: topo_components"
        try:
            response=ConnectionsConnectionConnectionidPathTopo_ComponentsEndpointidImpl.delete(connectionId, endpointId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, connectionId, endpointId):
        print "Retrieve operation of resource: topo_components"
        try:
            response = ConnectionsConnectionConnectionidPathTopo_ComponentsEndpointidImpl.get(connectionId, endpointId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/aEnd/
class CallsCallCallidAendMethodView(MethodView):

    def put(self, callId):
        print "Update operation of resource: aEnd"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = CallsCallCallidAendImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(Endpoint, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidAendImpl.put(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    CallsCallCallidAendImpl.put(callId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, callId):
        print "Create operation of resource: aEnd"
        try:
            response = CallsCallCallidAendImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(Endpoint, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidAendImpl.post(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, callId):
        print "Delete operation of resource: aEnd"
        try:
            response=CallsCallCallidAendImpl.delete(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, callId):
        print "Retrieve operation of resource: aEnd"
        try:
            response = CallsCallCallidAendImpl.get(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/match/include_path/label/
class CallsCallCallidMatchInclude_PathLabelMethodView(MethodView):

    def put(self, callId):
        print "Update operation of resource: label"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = CallsCallCallidMatchInclude_PathLabelImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(Label, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidMatchInclude_PathLabelImpl.put(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    CallsCallCallidMatchInclude_PathLabelImpl.put(callId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, callId):
        print "Create operation of resource: label"
        try:
            response = CallsCallCallidMatchInclude_PathLabelImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(Label, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidMatchInclude_PathLabelImpl.post(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, callId):
        print "Delete operation of resource: label"
        try:
            response=CallsCallCallidMatchInclude_PathLabelImpl.delete(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, callId):
        print "Retrieve operation of resource: label"
        try:
            response = CallsCallCallidMatchInclude_PathLabelImpl.get(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/calls/call/(\w+)/zEnd/
class CallsCallCallidZendMethodView(MethodView):

    def put(self, callId):
        print "Update operation of resource: zEnd"
        json_struct = request.get_json() #json parser.
        try:
            existing_object = CallsCallCallidZendImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            new_object = create_instance(Endpoint, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidZendImpl.put(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            existing_object = modify_instance(existing_object, json_struct)
            if isinstance(existing_object, BadRequestError):
                return existing_object
            elif isinstance(existing_object, NotFoundError):
                return existing_object
            else:
                try:
                    CallsCallCallidZendImpl.put(callId, existing_object)
                    js=existing_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")

        return Successful("Successful operation",json_dumps(js))



    def post(self, callId):
        print "Create operation of resource: zEnd"
        try:
            response = CallsCallCallidZendImpl.get(callId)
        except KeyError as inst:
            if inst.args[0] != 'callId':
                return NotFoundError(inst.args[0] + " not found")

            json_struct = request.get_json() #json parser.
            new_object = create_instance(Endpoint, json_struct)
            if isinstance(new_object, BadRequestError):
                return new_object
            elif isinstance(new_object, NotFoundError):
                return new_object
            else:
                try:
                    CallsCallCallidZendImpl.post(callId, new_object)
                    js=new_object.json_serializer()
                except KeyError as inst:
                    return NotFoundError(inst.args[0] + " not found")
        else:
            return BadRequestError("Object already exists. For updates use PUT.")
        return Successful("Successful operation",json_dumps(js))


    def delete(self, callId):
        print "Delete operation of resource: zEnd"
        try:
            response=CallsCallCallidZendImpl.delete(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            return Successful('Successful operation')


    def get(self, callId):
        print "Retrieve operation of resource: zEnd"
        try:
            response = CallsCallCallidZendImpl.get(callId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))



getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/", view_func = globals()["ConnectionsConnectionMethodView"].as_view('"ConnectionsConnection"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/<connectionId>/match/include_path/label/", view_func = globals()["CallsCallCallidConnectionsConnectionidMatchInclude_PathLabelMethodView"].as_view('"CallsCallCallidConnectionsConnectionidMatchInclude_PathLabel"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/traffic_params/", view_func = globals()["CallsCallCallidTraffic_ParamsMethodView"].as_view('"CallsCallCallidTraffic_Params"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/<connectionId>/match/", view_func = globals()["CallsCallCallidConnectionsConnectionidMatchMethodView"].as_view('"CallsCallCallidConnectionsConnectionidMatch"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/<connectionId>/traffic_params/", view_func = globals()["ConnectionsConnectionConnectionidTraffic_ParamsMethodView"].as_view('"ConnectionsConnectionConnectionidTraffic_Params"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/<connectionId>/match/include_path/topo_components/", view_func = globals()["CallsCallCallidConnectionsConnectionidMatchInclude_PathTopo_ComponentsMethodView"].as_view('"CallsCallCallidConnectionsConnectionidMatchInclude_PathTopo_Components"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/<connectionId>/traffic_params/", view_func = globals()["CallsCallCallidConnectionsConnectionidTraffic_ParamsMethodView"].as_view('"CallsCallCallidConnectionsConnectionidTraffic_Params"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/<connectionId>/path/topo_components/<endpointId>/", view_func = globals()["CallsCallCallidConnectionsConnectionidPathTopo_ComponentsEndpointidMethodView"].as_view('"CallsCallCallidConnectionsConnectionidPathTopo_ComponentsEndpointid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/<connectionId>/match/include_path/", view_func = globals()["CallsCallCallidConnectionsConnectionidMatchInclude_PathMethodView"].as_view('"CallsCallCallidConnectionsConnectionidMatchInclude_Path"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/<connectionId>/zEnd/", view_func = globals()["CallsCallCallidConnectionsConnectionidZendMethodView"].as_view('"CallsCallCallidConnectionsConnectionidZend"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/<connectionId>/aEnd/", view_func = globals()["ConnectionsConnectionConnectionidAendMethodView"].as_view('"ConnectionsConnectionConnectionidAend"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/transport_layer/", view_func = globals()["CallsCallCallidTransport_LayerMethodView"].as_view('"CallsCallCallidTransport_Layer"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/<connectionId>/match/include_path/topo_components/<endpointId>/", view_func = globals()["ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsEndpointidMethodView"].as_view('"ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsEndpointid"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/<connectionId>/", view_func = globals()["CallsCallCallidConnectionsConnectionidMethodView"].as_view('"CallsCallCallidConnectionsConnectionid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/", view_func = globals()["CallsMethodView"].as_view('"Calls"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/match/include_path/topo_components/<endpointId>/", view_func = globals()["CallsCallCallidMatchInclude_PathTopo_ComponentsEndpointidMethodView"].as_view('"CallsCallCallidMatchInclude_PathTopo_ComponentsEndpointid"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/<connectionId>/match/include_path/label/", view_func = globals()["ConnectionsConnectionConnectionidMatchInclude_PathLabelMethodView"].as_view('"ConnectionsConnectionConnectionidMatchInclude_PathLabel"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/<connectionId>/transport_layer/", view_func = globals()["ConnectionsConnectionConnectionidTransport_LayerMethodView"].as_view('"ConnectionsConnectionConnectionidTransport_Layer"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/<connectionId>/", view_func = globals()["ConnectionsConnectionConnectionidMethodView"].as_view('"ConnectionsConnectionConnectionid"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/<connectionId>/path/label/", view_func = globals()["CallsCallCallidConnectionsConnectionidPathLabelMethodView"].as_view('"CallsCallCallidConnectionsConnectionidPathLabel"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/<connectionId>/path/", view_func = globals()["ConnectionsConnectionConnectionidPathMethodView"].as_view('"ConnectionsConnectionConnectionidPath"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/match/include_path/topo_components/", view_func = globals()["CallsCallCallidMatchInclude_PathTopo_ComponentsMethodView"].as_view('"CallsCallCallidMatchInclude_PathTopo_Components"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/match/", view_func = globals()["CallsCallCallidMatchMethodView"].as_view('"CallsCallCallidMatch"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/", view_func = globals()["CallsCallCallidConnectionsMethodView"].as_view('"CallsCallCallidConnections"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/<connectionId>/match/include_path/topo_components/<endpointId>/", view_func = globals()["CallsCallCallidConnectionsConnectionidMatchInclude_PathTopo_ComponentsEndpointidMethodView"].as_view('"CallsCallCallidConnectionsConnectionidMatchInclude_PathTopo_ComponentsEndpointid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/<connectionId>/path/topo_components/", view_func = globals()["CallsCallCallidConnectionsConnectionidPathTopo_ComponentsMethodView"].as_view('"CallsCallCallidConnectionsConnectionidPathTopo_Components"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/<connectionId>/aEnd/", view_func = globals()["CallsCallCallidConnectionsConnectionidAendMethodView"].as_view('"CallsCallCallidConnectionsConnectionidAend"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/<connectionId>/match/include_path/topo_components/", view_func = globals()["ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsMethodView"].as_view('"ConnectionsConnectionConnectionidMatchInclude_PathTopo_Components"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/<connectionId>/path/", view_func = globals()["CallsCallCallidConnectionsConnectionidPathMethodView"].as_view('"CallsCallCallidConnectionsConnectionidPath"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/", view_func = globals()["CallsCallCallidMethodView"].as_view('"CallsCallCallid"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/<connectionId>/zEnd/", view_func = globals()["ConnectionsConnectionConnectionidZendMethodView"].as_view('"ConnectionsConnectionConnectionidZend"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/<connectionId>/path/topo_components/", view_func = globals()["ConnectionsConnectionConnectionidPathTopo_ComponentsMethodView"].as_view('"ConnectionsConnectionConnectionidPathTopo_Components"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/", view_func = globals()["CallsCallMethodView"].as_view('"CallsCall"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/", view_func = globals()["ConnectionsMethodView"].as_view('"Connections"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/<connectionId>/path/label/", view_func = globals()["ConnectionsConnectionConnectionidPathLabelMethodView"].as_view('"ConnectionsConnectionConnectionidPathLabel"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/<connectionId>/match/", view_func = globals()["ConnectionsConnectionConnectionidMatchMethodView"].as_view('"ConnectionsConnectionConnectionidMatch"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/connections/<connectionId>/transport_layer/", view_func = globals()["CallsCallCallidConnectionsConnectionidTransport_LayerMethodView"].as_view('"CallsCallCallidConnectionsConnectionidTransport_Layer"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/<connectionId>/match/include_path/", view_func = globals()["ConnectionsConnectionConnectionidMatchInclude_PathMethodView"].as_view('"ConnectionsConnectionConnectionidMatchInclude_Path"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/match/include_path/", view_func = globals()["CallsCallCallidMatchInclude_PathMethodView"].as_view('"CallsCallCallidMatchInclude_Path"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/connections/connection/<connectionId>/path/topo_components/<endpointId>/", view_func = globals()["ConnectionsConnectionConnectionidPathTopo_ComponentsEndpointidMethodView"].as_view('"ConnectionsConnectionConnectionidPathTopo_ComponentsEndpointid"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/aEnd/", view_func = globals()["CallsCallCallidAendMethodView"].as_view('"CallsCallCallidAend"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/match/include_path/label/", view_func = globals()["CallsCallCallidMatchInclude_PathLabelMethodView"].as_view('"CallsCallCallidMatchInclude_PathLabel"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/calls/call/<callId>/zEnd/", view_func = globals()["CallsCallCallidZendMethodView"].as_view('"CallsCallCallidZend"'+'"_api"'), methods=['PUT', 'POST', 'DELETE', 'GET'])
