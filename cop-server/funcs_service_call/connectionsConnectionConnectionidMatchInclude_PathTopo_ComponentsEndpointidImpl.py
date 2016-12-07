import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class ConnectionsConnectionConnectionidMatchInclude_PathTopo_ComponentsEndpointidImpl:

    @classmethod
    def put(cls, connectionId, endpointId, endpoint):
        print str(endpoint)
        print 'handling put'
        if connectionId in connections.connection:
            be.connections.connection[connectionId].match.includePath.topoComponents[endpointId] = endpoint
        else:
            raise KeyError('endpointId')

    @classmethod
    def post(cls, connectionId, endpointId, endpoint):
        print str(endpoint)
        print 'handling post'
        if connectionId in connections.connection:
            be.connections.connection[connectionId].match.includePath.topoComponents[endpointId] = endpoint
        else:
            raise KeyError('endpointId')

    @classmethod
    def delete(cls, connectionId, endpointId):
        print 'handling delete'
        if connectionId in be.connections.connection:
            if endpointId in be.connections.connection[connectionId].match.includePath.topoComponents:
                del be.connections.connection[connectionId].match.includePath.topoComponents[endpointId]
            else:
                raise KeyError('endpointId')
        else:
            raise KeyError('connectionId')

    @classmethod
    def get(cls, connectionId, endpointId):
        print 'handling get'
        if connectionId in be.connections.connection:
            if endpointId in be.connections.connection[connectionId].match.includePath.topoComponents:
                return be.connections.connection[connectionId].match.includePath.topoComponents[endpointId]
            else:
                raise KeyError('endpointId')
        else:
            raise KeyError('connectionId')
