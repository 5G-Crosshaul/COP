from flask import json, Blueprint, request, Response
from flask.views import MethodView
import sys
from objects_common.keyedArrayType import KeyedArrayKeyError

import base64
import re

# BACKEND FUNCTIONS
from funcs_service_topology.topologiesTopologyTopologyidEdgesEdgeidSourceEdge_EndEdgeendidImpl import TopologiesTopologyTopologyidEdgesEdgeidSourceEdge_EndEdgeendidImpl
from funcs_service_topology.topologiesTopologyTopologyidEdgesEdgeidImpl import TopologiesTopologyTopologyidEdgesEdgeidImpl
from funcs_service_topology.topologiesTopologyTopologyidNodesNodeidEdge_EndImpl import TopologiesTopologyTopologyidNodesNodeidEdge_EndImpl
from funcs_service_topology.topologiesTopologyTopologyidImpl import TopologiesTopologyTopologyidImpl
from funcs_service_topology.topologiesTopologyTopologyidNodesImpl import TopologiesTopologyTopologyidNodesImpl
from funcs_service_topology.topologiesService_End_PointSepidImpl import TopologiesService_End_PointSepidImpl
from funcs_service_topology.topologiesImpl import TopologiesImpl
from funcs_service_topology.topologiesTopologyImpl import TopologiesTopologyImpl
from funcs_service_topology.topologiesTopologyTopologyidEdgesEdgeidTargetImpl import TopologiesTopologyTopologyidEdgesEdgeidTargetImpl
from funcs_service_topology.topologiesTopologyTopologyidEdgesImpl import TopologiesTopologyTopologyidEdgesImpl
from funcs_service_topology.topologiesTopologyTopologyidEdgesEdgeidTargetEdge_EndImpl import TopologiesTopologyTopologyidEdgesEdgeidTargetEdge_EndImpl
from funcs_service_topology.topologiesTopologyTopologyidEdgesEdgeidTargetEdge_EndEdgeendidImpl import TopologiesTopologyTopologyidEdgesEdgeidTargetEdge_EndEdgeendidImpl
from funcs_service_topology.topologiesTopologyTopologyidEdgesEdgeidRemote_IfidImpl import TopologiesTopologyTopologyidEdgesEdgeidRemote_IfidImpl
from funcs_service_topology.topologiesTopologyTopologyidEdgesEdgeidSourceEdge_EndImpl import TopologiesTopologyTopologyidEdgesEdgeidSourceEdge_EndImpl
from funcs_service_topology.topologiesTopologyTopologyidEdgesEdgeidLocal_IfidImpl import TopologiesTopologyTopologyidEdgesEdgeidLocal_IfidImpl
from funcs_service_topology.topologiesService_End_PointImpl import TopologiesService_End_PointImpl
from funcs_service_topology.topologiesTopologyTopologyidNodesNodeidImpl import TopologiesTopologyTopologyidNodesNodeidImpl
from funcs_service_topology.topologiesTopologyTopologyidEdgesEdgeidSourceImpl import TopologiesTopologyTopologyidEdgesEdgeidSourceImpl
from funcs_service_topology.topologiesTopologyTopologyidNodesNodeidEdge_EndEdgeendidImpl import TopologiesTopologyTopologyidNodesNodeidEdge_EndEdgeendidImpl

# CALLABLE OBJECTS
from objects_service_topology.node import Node
from objects_service_topology.ethEdge import EthEdge
from objects_service_topology.edgeEnd import EdgeEnd
from objects_service_topology.topologiesSchema import TopologiesSchema
from objects_service_topology.bitmap import Bitmap
from objects_service_topology.dwdmChannel import DwdmChannel
from objects_service_topology.serviceEndPointType import ServiceEndPointType
from objects_service_topology.edge import Edge
from objects_service_topology.dwdmEdge import DwdmEdge
from objects_service_topology.topology import Topology

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


#/restconf/config/topologies/topology/(\w+)/edges/(\w+)/source/edge_end/(\w+)/
class TopologiesTopologyTopologyidEdgesEdgeidSourceEdge_EndEdgeendidMethodView(MethodView):

    def get(self, topologyId, edgeId, edgeEndId):
        print "Retrieve operation of resource: edge_end"
        try:
            response = TopologiesTopologyTopologyidEdgesEdgeidSourceEdge_EndEdgeendidImpl.get(topologyId, edgeId, edgeEndId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/(\w+)/edges/(\w+)/
class TopologiesTopologyTopologyidEdgesEdgeidMethodView(MethodView):

    def get(self, topologyId, edgeId):
        print "Retrieve operation of resource: edges"
        try:
            response = TopologiesTopologyTopologyidEdgesEdgeidImpl.get(topologyId, edgeId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/(\w+)/nodes/(\w+)/edge_end/
class TopologiesTopologyTopologyidNodesNodeidEdge_EndMethodView(MethodView):

    def get(self, topologyId, nodeId):
        print "Retrieve operation of resource: edge_end"
        try:
            response = TopologiesTopologyTopologyidNodesNodeidEdge_EndImpl.get(topologyId, nodeId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/(\w+)/
class TopologiesTopologyTopologyidMethodView(MethodView):

    def get(self, topologyId):
        print "Retrieve operation of resource: topology"
        try:
            response = TopologiesTopologyTopologyidImpl.get(topologyId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/(\w+)/nodes/
class TopologiesTopologyTopologyidNodesMethodView(MethodView):

    def get(self, topologyId):
        print "Retrieve operation of resource: nodes"
        try:
            response = TopologiesTopologyTopologyidNodesImpl.get(topologyId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/service_end_point/(\w+)/
class TopologiesService_End_PointSepidMethodView(MethodView):

    def get(self, sepId):
        print "Retrieve operation of resource: service_end_point"
        try:
            response = TopologiesService_End_PointSepidImpl.get(sepId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/
class TopologiesMethodView(MethodView):

    def get(self, ):
        print "Retrieve operation of resource: topologies"
        try:
            response = TopologiesImpl.get()
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/
class TopologiesTopologyMethodView(MethodView):

    def get(self, ):
        print "Retrieve operation of resource: topology"
        try:
            response = TopologiesTopologyImpl.get()
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/(\w+)/edges/(\w+)/target/
class TopologiesTopologyTopologyidEdgesEdgeidTargetMethodView(MethodView):

    def get(self, topologyId, edgeId):
        print "Retrieve operation of resource: target"
        try:
            response = TopologiesTopologyTopologyidEdgesEdgeidTargetImpl.get(topologyId, edgeId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/(\w+)/edges/
class TopologiesTopologyTopologyidEdgesMethodView(MethodView):

    def get(self, topologyId):
        print "Retrieve operation of resource: edges"
        try:
            response = TopologiesTopologyTopologyidEdgesImpl.get(topologyId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/(\w+)/edges/(\w+)/target/edge_end/
class TopologiesTopologyTopologyidEdgesEdgeidTargetEdge_EndMethodView(MethodView):

    def get(self, topologyId, edgeId):
        print "Retrieve operation of resource: edge_end"
        try:
            response = TopologiesTopologyTopologyidEdgesEdgeidTargetEdge_EndImpl.get(topologyId, edgeId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/(\w+)/edges/(\w+)/target/edge_end/(\w+)/
class TopologiesTopologyTopologyidEdgesEdgeidTargetEdge_EndEdgeendidMethodView(MethodView):

    def get(self, topologyId, edgeId, edgeEndId):
        print "Retrieve operation of resource: edge_end"
        try:
            response = TopologiesTopologyTopologyidEdgesEdgeidTargetEdge_EndEdgeendidImpl.get(topologyId, edgeId, edgeEndId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/(\w+)/edges/(\w+)/remote_ifid/
class TopologiesTopologyTopologyidEdgesEdgeidRemote_IfidMethodView(MethodView):

    def get(self, topologyId, edgeId):
        print "Retrieve operation of resource: remote_ifid"
        try:
            response = TopologiesTopologyTopologyidEdgesEdgeidRemote_IfidImpl.get(topologyId, edgeId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/(\w+)/edges/(\w+)/source/edge_end/
class TopologiesTopologyTopologyidEdgesEdgeidSourceEdge_EndMethodView(MethodView):

    def get(self, topologyId, edgeId):
        print "Retrieve operation of resource: edge_end"
        try:
            response = TopologiesTopologyTopologyidEdgesEdgeidSourceEdge_EndImpl.get(topologyId, edgeId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/(\w+)/edges/(\w+)/local_ifid/
class TopologiesTopologyTopologyidEdgesEdgeidLocal_IfidMethodView(MethodView):

    def get(self, topologyId, edgeId):
        print "Retrieve operation of resource: local_ifid"
        try:
            response = TopologiesTopologyTopologyidEdgesEdgeidLocal_IfidImpl.get(topologyId, edgeId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/service_end_point/
class TopologiesService_End_PointMethodView(MethodView):

    def get(self, ):
        print "Retrieve operation of resource: service_end_point"
        try:
            response = TopologiesService_End_PointImpl.get()
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/(\w+)/nodes/(\w+)/
class TopologiesTopologyTopologyidNodesNodeidMethodView(MethodView):

    def get(self, topologyId, nodeId):
        print "Retrieve operation of resource: nodes"
        try:
            response = TopologiesTopologyTopologyidNodesNodeidImpl.get(topologyId, nodeId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/(\w+)/edges/(\w+)/source/
class TopologiesTopologyTopologyidEdgesEdgeidSourceMethodView(MethodView):

    def get(self, topologyId, edgeId):
        print "Retrieve operation of resource: source"
        try:
            response = TopologiesTopologyTopologyidEdgesEdgeidSourceImpl.get(topologyId, edgeId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))


#/restconf/config/topologies/topology/(\w+)/nodes/(\w+)/edge_end/(\w+)/
class TopologiesTopologyTopologyidNodesNodeidEdge_EndEdgeendidMethodView(MethodView):

    def get(self, topologyId, nodeId, edgeEndId):
        print "Retrieve operation of resource: edge_end"
        try:
            response = TopologiesTopologyTopologyidNodesNodeidEdge_EndEdgeendidImpl.get(topologyId, nodeId, edgeEndId)
        except KeyError as inst:
            return NotFoundError(inst.args[0] + " not found")
        else:
            js = response.json_serializer()
            return Successful("Successful operation",json_dumps(js))



getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/edges/<edgeId>/source/edge_end/<edgeEndId>/", view_func = globals()["TopologiesTopologyTopologyidEdgesEdgeidSourceEdge_EndEdgeendidMethodView"].as_view('"TopologiesTopologyTopologyidEdgesEdgeidSourceEdge_EndEdgeendid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/edges/<edgeId>/", view_func = globals()["TopologiesTopologyTopologyidEdgesEdgeidMethodView"].as_view('"TopologiesTopologyTopologyidEdgesEdgeid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/nodes/<nodeId>/edge_end/", view_func = globals()["TopologiesTopologyTopologyidNodesNodeidEdge_EndMethodView"].as_view('"TopologiesTopologyTopologyidNodesNodeidEdge_End"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/", view_func = globals()["TopologiesTopologyTopologyidMethodView"].as_view('"TopologiesTopologyTopologyid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/nodes/", view_func = globals()["TopologiesTopologyTopologyidNodesMethodView"].as_view('"TopologiesTopologyTopologyidNodes"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/service_end_point/<sepId>/", view_func = globals()["TopologiesService_End_PointSepidMethodView"].as_view('"TopologiesService_End_PointSepid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/", view_func = globals()["TopologiesMethodView"].as_view('"Topologies"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/", view_func = globals()["TopologiesTopologyMethodView"].as_view('"TopologiesTopology"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/edges/<edgeId>/target/", view_func = globals()["TopologiesTopologyTopologyidEdgesEdgeidTargetMethodView"].as_view('"TopologiesTopologyTopologyidEdgesEdgeidTarget"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/edges/", view_func = globals()["TopologiesTopologyTopologyidEdgesMethodView"].as_view('"TopologiesTopologyTopologyidEdges"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/edges/<edgeId>/target/edge_end/", view_func = globals()["TopologiesTopologyTopologyidEdgesEdgeidTargetEdge_EndMethodView"].as_view('"TopologiesTopologyTopologyidEdgesEdgeidTargetEdge_End"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/edges/<edgeId>/target/edge_end/<edgeEndId>/", view_func = globals()["TopologiesTopologyTopologyidEdgesEdgeidTargetEdge_EndEdgeendidMethodView"].as_view('"TopologiesTopologyTopologyidEdgesEdgeidTargetEdge_EndEdgeendid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/edges/<edgeId>/remote_ifid/", view_func = globals()["TopologiesTopologyTopologyidEdgesEdgeidRemote_IfidMethodView"].as_view('"TopologiesTopologyTopologyidEdgesEdgeidRemote_Ifid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/edges/<edgeId>/source/edge_end/", view_func = globals()["TopologiesTopologyTopologyidEdgesEdgeidSourceEdge_EndMethodView"].as_view('"TopologiesTopologyTopologyidEdgesEdgeidSourceEdge_End"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/edges/<edgeId>/local_ifid/", view_func = globals()["TopologiesTopologyTopologyidEdgesEdgeidLocal_IfidMethodView"].as_view('"TopologiesTopologyTopologyidEdgesEdgeidLocal_Ifid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/service_end_point/", view_func = globals()["TopologiesService_End_PointMethodView"].as_view('"TopologiesService_End_Point"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/nodes/<nodeId>/", view_func = globals()["TopologiesTopologyTopologyidNodesNodeidMethodView"].as_view('"TopologiesTopologyTopologyidNodesNodeid"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/edges/<edgeId>/source/", view_func = globals()["TopologiesTopologyTopologyidEdgesEdgeidSourceMethodView"].as_view('"TopologiesTopologyTopologyidEdgesEdgeidSource"'+'"_api"'), methods=['GET'])
getattr(sys.modules[__name__], __name__).add_url_rule("/restconf/config/topologies/topology/<topologyId>/nodes/<nodeId>/edge_end/<edgeEndId>/", view_func = globals()["TopologiesTopologyTopologyidNodesNodeidEdge_EndEdgeendidMethodView"].as_view('"TopologiesTopologyTopologyidNodesNodeidEdge_EndEdgeendid"'+'"_api"'), methods=['GET'])
