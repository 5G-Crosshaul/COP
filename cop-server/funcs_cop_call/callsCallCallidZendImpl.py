import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class CallsCallCallidZendImpl:

    @classmethod
    def put(cls, callId, endpoint):
        print str(endpoint)
        print 'handling put'
        be.calls.call[callId] = endpoint

    @classmethod
    def post(cls, callId, endpoint):
        print str(endpoint)
        print 'handling post'
        be.calls.call[callId] = endpoint

    @classmethod
    def delete(cls, callId):
        print 'handling delete'
        if callId in be.calls.call:
            del be.calls.call[callId].zEnd
        else:
            raise KeyError('callId')

    @classmethod
    def get(cls, callId):
        print 'handling get'
        if callId in be.calls.call:
            return be.calls.call[callId].zEnd
        else:
            raise KeyError('callId')
