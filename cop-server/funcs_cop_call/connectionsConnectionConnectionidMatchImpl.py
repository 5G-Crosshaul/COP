import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class ConnectionsConnectionConnectionidMatchImpl:

    @classmethod
    def put(cls, connectionId, matchrules):
        print str(matchrules)
        print 'handling put'
        be.connections.connection[connectionId] = matchrules

    @classmethod
    def post(cls, connectionId, matchrules):
        print str(matchrules)
        print 'handling post'
        be.connections.connection[connectionId] = matchrules

    @classmethod
    def delete(cls, connectionId):
        print 'handling delete'
        if connectionId in be.connections.connection:
            del be.connections.connection[connectionId].match
        else:
            raise KeyError('connectionId')

    @classmethod
    def get(cls, connectionId):
        print 'handling get'
        if connectionId in be.connections.connection:
            return be.connections.connection[connectionId].match
        else:
            raise KeyError('connectionId')
