import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class CallsCallCallidTransport_LayerImpl:

    @classmethod
    def put(cls, callId, transportlayertype):
        print str(transportlayertype)
        print 'handling put'
        be.calls.call[callId] = transportlayertype

    @classmethod
    def post(cls, callId, transportlayertype):
        print str(transportlayertype)
        print 'handling post'
        be.calls.call[callId] = transportlayertype

    @classmethod
    def delete(cls, callId):
        print 'handling delete'
        if callId in be.calls.call:
            del be.calls.call[callId].transportLayer
        else:
            raise KeyError('callId')

    @classmethod
    def get(cls, callId):
        print 'handling get'
        if callId in be.calls.call:
            return be.calls.call[callId].transportLayer
        else:
            raise KeyError('callId')
