import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class CallsCallCallidMatchInclude_PathTopo_ComponentsEndpointidImpl:

    @classmethod
    def put(cls, callId, endpointId, serviceendpoint):
        print str(serviceendpoint)
        print 'handling put'
        if callId in calls.call:
            be.calls.call[callId].match.includePath.topoComponents[endpointId] = serviceendpoint
        else:
            raise KeyError('endpointId')

    @classmethod
    def post(cls, callId, endpointId, serviceendpoint):
        print str(serviceendpoint)
        print 'handling post'
        if callId in calls.call:
            be.calls.call[callId].match.includePath.topoComponents[endpointId] = serviceendpoint
        else:
            raise KeyError('endpointId')

    @classmethod
    def delete(cls, callId, endpointId):
        print 'handling delete'
        if callId in be.calls.call:
            if endpointId in be.calls.call[callId].match.includePath.topoComponents:
                del be.calls.call[callId].match.includePath.topoComponents[endpointId]
            else:
                raise KeyError('endpointId')
        else:
            raise KeyError('callId')

    @classmethod
    def get(cls, callId, endpointId):
        print 'handling get'
        if callId in be.calls.call:
            if endpointId in be.calls.call[callId].match.includePath.topoComponents:
                return be.calls.call[callId].match.includePath.topoComponents[endpointId]
            else:
                raise KeyError('endpointId')
        else:
            raise KeyError('callId')
