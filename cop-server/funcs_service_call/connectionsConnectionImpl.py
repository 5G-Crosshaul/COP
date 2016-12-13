import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class ConnectionsConnectionImpl:

    @classmethod
    def get(cls, ):
        print 'handling get'
        if be.connections:
            return be.connections
        else:
            raise KeyError('')
