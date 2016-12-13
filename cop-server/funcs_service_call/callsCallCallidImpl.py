import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class CallsCallCallidImpl:

    @classmethod
    def put(cls, callId, call):
        print str(call)
        print 'handling put'
        be.calls.call[callId] = call

    @classmethod
    def post(cls, callId, call):
        print str(call)
        print 'handling post'
        be.calls.call[callId] = call

    @classmethod
    def delete(cls, callId):
        print 'handling delete'
        if callId in be.calls.call:
            del be.calls.call[callId]
        else:
            raise KeyError('callId')

    @classmethod
    def get(cls, callId):
        print 'handling get'
        if callId in be.calls.call:
            return be.calls.call[callId]
        else:
            raise KeyError('callId')
