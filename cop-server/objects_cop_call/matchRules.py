from objects_common.jsonObject import JsonObject
from pathType import PathType

class MatchRules(JsonObject):

    def __init__(self, json_struct=None):
        self.inPhyPort=""
        self.ethSrc=""
        self.icmpv6Type=0
        self.ipEcn=0
        self.icmpv4Type=0
        self.ethDst=""
        self.vlanPcp=0
        self.ipv4Dst=""
        self.arpTpa=0
        self.arpSha=0
        self.ipv6Exthdr=0
        self.arpTha=0
        self.ipv6Src=""
        self.mplsTc=0
        self.tunnelId=0
        self.sctpDst=0
        self.mplsLabel=0
        self.ipv6NdTarget=0
        self.tcpSrc=0
        self.ipv4Src=""
        self.icmpv6Code=0
        self.mplsBos=0
        self.experimentalGmplsWsonLabel=0
        self.ipv6NdTll=0
        self.sctpSrc=0
        self.udpDst=0
        self.pbbIsid=0
        self.ipv6Flabel=""
        self.inPort=""
        self.icmpv4Code=0
        self.ipDscp=0
        self.ethType=0
        self.ipProto=0
        self.includePath=PathType() #import
        self.arpSpa=0
        self.ipv6Dst=""
        self.udpSrc=0
        self.arpOp=0
        self.ipv6NdSll=0
        self.vlanVid=0
        self.experimentalTeid=0
        self.metadata=""
        self.tcpDst=0
        super(MatchRules, self).__init__(json_struct)

