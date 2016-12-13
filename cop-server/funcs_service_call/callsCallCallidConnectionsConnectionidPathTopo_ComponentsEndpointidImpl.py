import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class CallsCallCallidConnectionsConnectionidPathTopo_ComponentsEndpointidImpl:

    @classmethod
    def get(cls, callId, connectionId, endpointId):
        print 'handling get'
        if callId in be.calls.call:
            if connectionId in be.calls.call[callId].connections:
                if endpointId in be.calls.call[callId].connections[connectionId].path.topoComponents:
                    return be.calls.call[callId].connections[connectionId].path.topoComponents[endpointId]
                else:
                    raise KeyError('endpointId')
            else:
                raise KeyError('connectionId')
        else:
            raise KeyError('callId')
