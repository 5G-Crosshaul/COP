import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class ConnectionsConnectionConnectionidZendImpl:

    @classmethod
    def put(cls, connectionId, serviceendpoint):
        print str(serviceendpoint)
        print 'handling put'
        be.connections.connection[connectionId] = serviceendpoint

    @classmethod
    def post(cls, connectionId, serviceendpoint):
        print str(serviceendpoint)
        print 'handling post'
        be.connections.connection[connectionId] = serviceendpoint

    @classmethod
    def delete(cls, connectionId):
        print 'handling delete'
        if connectionId in be.connections.connection:
            del be.connections.connection[connectionId].zEnd
        else:
            raise KeyError('connectionId')

    @classmethod
    def get(cls, connectionId):
        print 'handling get'
        if connectionId in be.connections.connection:
            return be.connections.connection[connectionId].zEnd
        else:
            raise KeyError('connectionId')
