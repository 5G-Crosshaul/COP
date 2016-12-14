import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class CallsCallCallidMatchInclude_PathImpl:

    @classmethod
    def put(cls, callId, pathtype):
        print str(pathtype)
        print 'handling put'
        be.calls.call[callId] = pathtype

    @classmethod
    def post(cls, callId, pathtype):
        print str(pathtype)
        print 'handling post'
        be.calls.call[callId] = pathtype

    @classmethod
    def delete(cls, callId):
        print 'handling delete'
        if callId in be.calls.call:
            del be.calls.call[callId].match.includePath
        else:
            raise KeyError('callId')

    @classmethod
    def get(cls, callId):
        print 'handling get'
        if callId in be.calls.call:
            return be.calls.call[callId].match.includePath
        else:
            raise KeyError('callId')
