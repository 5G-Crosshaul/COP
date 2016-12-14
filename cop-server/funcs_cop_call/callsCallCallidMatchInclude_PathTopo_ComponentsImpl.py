import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class CallsCallCallidMatchInclude_PathTopo_ComponentsImpl:

    @classmethod
    def get(cls, callId):
        print 'handling get'
        if callId in be.calls.call:
            return be.calls.call[callId].match.includePath.topoComponents
        else:
            raise KeyError('callId')
