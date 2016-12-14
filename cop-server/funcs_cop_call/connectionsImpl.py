import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class ConnectionsImpl:

    @classmethod
    def put(cls, connectionsschema):
        print str(connectionsschema)
        print 'handling put'
        be.connections = connectionsschema

    @classmethod
    def post(cls, connectionsschema):
        print str(connectionsschema)
        print 'handling post'
        be.connections = connectionsschema

    @classmethod
    def delete(cls, ):
        print 'handling delete'
        if be.connections:
            del be.connections
        else:
            raise KeyError('')

    @classmethod
    def get(cls, ):
        print 'handling get'
        if be.connections:
            return be.connections
        else:
            raise KeyError('')
