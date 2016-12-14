import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class TopologiesService_End_PointSepidImpl:

    @classmethod
    def get(cls, sepId):
        print 'handling get'
        if sepId in be.topologies.serviceEndPoint:
            return be.topologies.serviceEndPoint[sepId]
        else:
            raise KeyError('sepId')
