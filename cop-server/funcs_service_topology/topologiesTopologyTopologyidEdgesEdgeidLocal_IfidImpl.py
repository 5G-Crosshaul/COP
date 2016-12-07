import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class TopologiesTopologyTopologyidEdgesEdgeidLocal_IfidImpl:

    @classmethod
    def get(cls, topologyId, edgeId):
        print 'handling get'
        if topologyId in be.topologies.topology:
            if edgeId in be.topologies.topology[topologyId].edges:
                return be.topologies.topology[topologyId].edges[edgeId].localIfid
            else:
                raise KeyError('edgeId')
        else:
            raise KeyError('topologyId')
