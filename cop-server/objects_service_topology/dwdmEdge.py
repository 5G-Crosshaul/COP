from dwdmChannel import DwdmChannel
from bitmap import Bitmap
from edge import Edge
from objects_common.keyedArrayType import KeyedArrayType

class DwdmEdge(Edge):

    def __init__(self, json_struct=None):
        self.channels=KeyedArrayType(DwdmChannel, 'g694Id')
        self.bitmap=Bitmap() #import
        super(DwdmEdge, self).__init__(json_struct)

