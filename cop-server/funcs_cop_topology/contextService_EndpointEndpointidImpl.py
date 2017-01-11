import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class ContextService_EndpointEndpointidImpl:

    @classmethod
    def get(cls, endpointId):
        print 'handling get'
        if endpointId in be.context.serviceEndpoint:
            return be.context.serviceEndpoint[endpointId]
        else:
            raise KeyError('endpointId')
