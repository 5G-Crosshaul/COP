import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class TopologiesTopologyTopologyidNodesNodeidEdge_EndImpl:

    @classmethod
    def get(cls, topologyId, nodeId):
        print 'handling get'
        if topologyId in be.topologies.topology:
            if nodeId in be.topologies.topology[topologyId].nodes:
                return be.topologies.topology[topologyId].nodes[nodeId].edgeEnd
            else:
                raise KeyError('nodeId')
        else:
            raise KeyError('topologyId')
