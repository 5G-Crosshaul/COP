import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class CallsImpl:

    @classmethod
    def put(cls, callsschema):
        print str(callsschema)
        print 'handling put'
        be.calls = callsschema

    @classmethod
    def post(cls, callsschema):
        print str(callsschema)
        print 'handling post'
        be.calls = callsschema

    @classmethod
    def delete(cls, ):
        print 'handling delete'
        if be.calls:
            del be.calls
        else:
            raise KeyError('')

    @classmethod
    def get(cls, ):
        print 'handling get'
        if be.calls:
            return be.calls
        else:
            raise KeyError('')
