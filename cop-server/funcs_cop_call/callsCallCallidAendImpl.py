import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class CallsCallCallidAendImpl:

    @classmethod
    def put(cls, callId, serviceendpoint):
        print str(serviceendpoint)
        print 'handling put'
        be.calls.call[callId] = serviceendpoint

    @classmethod
    def post(cls, callId, serviceendpoint):
        print str(serviceendpoint)
        print 'handling post'
        be.calls.call[callId] = serviceendpoint

    @classmethod
    def delete(cls, callId):
        print 'handling delete'
        if callId in be.calls.call:
            del be.calls.call[callId].aEnd
        else:
            raise KeyError('callId')

    @classmethod
    def get(cls, callId):
        print 'handling get'
        if callId in be.calls.call:
            return be.calls.call[callId].aEnd
        else:
            raise KeyError('callId')
