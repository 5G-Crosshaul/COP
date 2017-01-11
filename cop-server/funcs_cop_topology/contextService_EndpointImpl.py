import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class ContextService_EndpointImpl:

    @classmethod
    def get(cls, ):
        print 'handling get'
        if be.context:
            return be.context
        else:
            raise KeyError('')
