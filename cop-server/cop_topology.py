from flask import json, Blueprint, request, Response
from flask.views import MethodView
import sys
from objects_common.keyedArrayType import KeyedArrayKeyError

import base64
import re

# BACKEND FUNCTIONS
from funcs_cop_topology.contextService_EndpointImpl import ContextService_EndpointImpl
from funcs_cop_topology.contextTopologyImpl import ContextTopologyImpl
from funcs_cop_topology.contextTopologyTopologyidNodesNodeidEdge_EndEdgeendidImpl import ContextTopologyTopologyidNodesNodeidEdge_EndEdgeendidImpl
from funcs_cop_topology.contextTopologyTopologyidEdgesEdgeidImpl import ContextTopologyTopologyidEdgesEdgeidImpl
from funcs_cop_topology.contextTopologyTopologyidNodesImpl import ContextTopologyTopologyidNodesImpl
from funcs_cop_topology.contextTopologyTopologyidNodesNodeidImpl import ContextTopologyTopologyidNodesNodeidImpl
from funcs_cop_topology.contextTopologyTopologyidNodesNodeidEdge_EndImpl import ContextTopologyTopologyidNodesNodeidEdge_EndImpl
from funcs_cop_topology.contextService_EndpointEndpointidImpl import ContextService_EndpointEndpointidImpl
from funcs_cop_topology.contextTopologyTopologyidImpl import ContextTopologyTopologyidImpl
from funcs_cop_topology.contextTopologyTopologyidEdgesImpl import ContextTopologyTopologyidEdgesImpl
from funcs_cop_topology.contextImpl import ContextImpl

# CALLABLE OBJECTS
from objects_cop_topology.node import Node
from objects_cop_topology.transportLayerType import TransportLayerType
from objects_cop_topology.wirelessEdge import WirelessEdge
from objects_cop_topology.ethEdge import EthEdge
from objects_cop_topology.trafficParams import TrafficParams
from objects_cop_topology.edgeEnd import EdgeEnd
from objects_cop_topology.pathType import PathType
from objects_cop_topology.bitmap import Bitmap
from objects_cop_topology.dwdmChannel import DwdmChannel
from objects_cop_topology.contextSchema import ContextSchema
from objects_cop_topology.connection import Connection
from objects_cop_topology.edge import Edge
from objects_cop_topology.call import Call
from objects_cop_topology.label import Label
from objects_cop_topology.serviceEndpoint import ServiceEndpoint
from objects_cop_topology.dwdmEdge import DwdmEdge
from objects_cop_topology.matchRules import MatchRules
from objects_cop_topology.topology import Topology

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


#/restconf/config/context/service_endpoint/
class ContextService_EndpointMethodView(MethodView):

    def get(self, ):
        print "Retrieve operation of resource: service_endpoint"
        try:
            response = ContextService_EndpointImpl.get()
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/context/topology/
class ContextTopologyMethodView(MethodView):

    def get(self, ):
        print "Retrieve operation of resource: topology"
        try:
            response = ContextTopologyImpl.get()
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/context/topology/(\w+)/nodes/(\w+)/edge_end/(\w+)/
class ContextTopologyTopologyidNodesNodeidEdge_EndEdgeendidMethodView(MethodView):

    def get(self, topologyId, nodeId, edgeEndId):
        print "Retrieve operation of resource: edge_end"
        try:
            response = ContextTopologyTopologyidNodesNodeidEdge_EndEdgeendidImpl.get(topologyId, nodeId, edgeEndId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/context/topology/(\w+)/edges/(\w+)/
class ContextTopologyTopologyidEdgesEdgeidMethodView(MethodView):

    def get(self, topologyId, edgeId):
        print "Retrieve operation of resource: edges"
        try:
            response = ContextTopologyTopologyidEdgesEdgeidImpl.get(topologyId, edgeId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/context/topology/(\w+)/nodes/
class ContextTopologyTopologyidNodesMethodView(MethodView):

    def get(self, topologyId):
        print "Retrieve operation of resource: nodes"
        try:
            response = ContextTopologyTopologyidNodesImpl.get(topologyId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/context/topology/(\w+)/nodes/(\w+)/
class ContextTopologyTopologyidNodesNodeidMethodView(MethodView):

    def get(self, topologyId, nodeId):
        print "Retrieve operation of resource: nodes"
        try:
            response = ContextTopologyTopologyidNodesNodeidImpl.get(topologyId, nodeId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/context/topology/(\w+)/nodes/(\w+)/edge_end/
class ContextTopologyTopologyidNodesNodeidEdge_EndMethodView(MethodView):

    def get(self, topologyId, nodeId):
        print "Retrieve operation of resource: edge_end"
        try:
            response = ContextTopologyTopologyidNodesNodeidEdge_EndImpl.get(topologyId, nodeId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/context/service_endpoint/(\w+)/
class ContextService_EndpointEndpointidMethodView(MethodView):

    def get(self, endpointId):
        print "Retrieve operation of resource: service_endpoint"
        try:
            response = ContextService_EndpointEndpointidImpl.get(endpointId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/context/topology/(\w+)/
class ContextTopologyTopologyidMethodView(MethodView):

    def get(self, topologyId):
        print "Retrieve operation of resource: topology"
        try:
            response = ContextTopologyTopologyidImpl.get(topologyId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/context/topology/(\w+)/edges/
class ContextTopologyTopologyidEdgesMethodView(MethodView):

    def get(self, topologyId):
        print "Retrieve operation of resource: edges"
        try:
            response = ContextTopologyTopologyidEdgesImpl.get(topologyId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/context/
class ContextMethodView(MethodView):

    def get(self, ):
        print "Retrieve operation of resource: context"
        try:
            response = ContextImpl.get()
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))



getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/context/service_endpoint/", view_func = globals()["ContextService_EndpointMethodView"].as_view('"ContextService_Endpoint"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/context/topology/", view_func = globals()["ContextTopologyMethodView"].as_view('"ContextTopology"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/context/topology/<topologyId>/nodes/<nodeId>/edge_end/<edgeEndId>/", view_func = globals()["ContextTopologyTopologyidNodesNodeidEdge_EndEdgeendidMethodView"].as_view('"ContextTopologyTopologyidNodesNodeidEdge_EndEdgeendid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/context/topology/<topologyId>/edges/<edgeId>/", view_func = globals()["ContextTopologyTopologyidEdgesEdgeidMethodView"].as_view('"ContextTopologyTopologyidEdgesEdgeid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/context/topology/<topologyId>/nodes/", view_func = globals()["ContextTopologyTopologyidNodesMethodView"].as_view('"ContextTopologyTopologyidNodes"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/context/topology/<topologyId>/nodes/<nodeId>/", view_func = globals()["ContextTopologyTopologyidNodesNodeidMethodView"].as_view('"ContextTopologyTopologyidNodesNodeid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/context/topology/<topologyId>/nodes/<nodeId>/edge_end/", view_func = globals()["ContextTopologyTopologyidNodesNodeidEdge_EndMethodView"].as_view('"ContextTopologyTopologyidNodesNodeidEdge_End"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/context/service_endpoint/<endpointId>/", view_func = globals()["ContextService_EndpointEndpointidMethodView"].as_view('"ContextService_EndpointEndpointid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/context/topology/<topologyId>/", view_func = globals()["ContextTopologyTopologyidMethodView"].as_view('"ContextTopologyTopologyid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/context/topology/<topologyId>/edges/", view_func = globals()["ContextTopologyTopologyidEdgesMethodView"].as_view('"ContextTopologyTopologyidEdges"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/context/", view_func = globals()["ContextMethodView"].as_view('"Context"'+'"_api"'), methods=['GET'])
