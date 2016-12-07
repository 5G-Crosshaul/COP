import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class TopologiesTopologyTopologyidEdgesEdgeidTargetEdge_EndEdgeendidImpl:

    @classmethod
    def get(cls, topologyId, edgeId, edgeEndId):
        print 'handling get'
        if topologyId in be.topologies.topology:
            if edgeId in be.topologies.topology[topologyId].edges:
                if edgeEndId in be.topologies.topology[topologyId].edges[edgeId].target.edgeEnd:
                    return be.topologies.topology[topologyId].edges[edgeId].target.edgeEnd[edgeEndId]
                else:
                    raise KeyError('edgeEndId')
            else:
                raise KeyError('edgeId')
        else:
            raise KeyError('topologyId')
