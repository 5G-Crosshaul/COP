import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class ConnectionsConnectionConnectionidTraffic_ParamsImpl:

    @classmethod
    def put(cls, connectionId, trafficparams):
        print str(trafficparams)
        print 'handling put'
        be.connections.connection[connectionId] = trafficparams

    @classmethod
    def post(cls, connectionId, trafficparams):
        print str(trafficparams)
        print 'handling post'
        be.connections.connection[connectionId] = trafficparams

    @classmethod
    def delete(cls, connectionId):
        print 'handling delete'
        if connectionId in be.connections.connection:
            del be.connections.connection[connectionId].trafficParams
        else:
            raise KeyError('connectionId')

    @classmethod
    def get(cls, connectionId):
        print 'handling get'
        if connectionId in be.connections.connection:
            return be.connections.connection[connectionId].trafficParams
        else:
            raise KeyError('connectionId')
