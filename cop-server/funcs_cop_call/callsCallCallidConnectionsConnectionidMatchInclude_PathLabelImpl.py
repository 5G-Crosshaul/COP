import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class CallsCallCallidConnectionsConnectionidMatchInclude_PathLabelImpl:

    @classmethod
    def get(cls, callId, connectionId):
        print 'handling get'
        if callId in be.calls.call:
            if connectionId in be.calls.call[callId].connections:
                return be.calls.call[callId].connections[connectionId].match.includePath.label
            else:
                raise KeyError('connectionId')
        else:
            raise KeyError('callId')
