import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class ContextTopologyTopologyidNodesNodeidEdge_EndEdgeendidImpl:

    @classmethod
    def get(cls, topologyId, nodeId, edgeEndId):
        print 'handling get'
        if topologyId in be.context.topology:
            if nodeId in be.context.topology[topologyId].nodes:
                if edgeEndId in be.context.topology[topologyId].nodes[nodeId].edgeEnd:
                    return be.context.topology[topologyId].nodes[nodeId].edgeEnd[edgeEndId]
                else:
                    raise KeyError('edgeEndId')
            else:
                raise KeyError('nodeId')
        else:
            raise KeyError('topologyId')
