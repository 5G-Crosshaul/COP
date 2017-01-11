import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class ContextTopologyTopologyidEdgesEdgeidImpl:

    @classmethod
    def get(cls, topologyId, edgeId):
        print 'handling get'
        if topologyId in be.context.topology:
            if edgeId in be.context.topology[topologyId].edges:
                return be.context.topology[topologyId].edges[edgeId]
            else:
                raise KeyError('edgeId')
        else:
            raise KeyError('topologyId')
