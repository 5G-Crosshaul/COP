import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class TopologiesTopologyTopologyidEdgesImpl:

    @classmethod
    def get(cls, topologyId):
        print 'handling get'
        if topologyId in be.topologies.topology:
            return be.topologies.topology[topologyId].edges
        else:
            raise KeyError('topologyId')
