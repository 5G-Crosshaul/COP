import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class ConnectionsConnectionConnectionidImpl:

    @classmethod
    def put(cls, connectionId, connection):
        print str(connection)
        print 'handling put'
        be.connections.connection[connectionId] = connection

    @classmethod
    def post(cls, connectionId, connection):
        print str(connection)
        print 'handling post'
        be.connections.connection[connectionId] = connection

    @classmethod
    def delete(cls, connectionId):
        print 'handling delete'
        if connectionId in be.connections.connection:
            del be.connections.connection[connectionId]
        else:
            raise KeyError('connectionId')

    @classmethod
    def get(cls, connectionId):
        print 'handling get'
        if connectionId in be.connections.connection:
            return be.connections.connection[connectionId]
        else:
            raise KeyError('connectionId')
