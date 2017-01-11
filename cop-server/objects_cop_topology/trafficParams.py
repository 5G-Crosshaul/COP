from objects_common.jsonObject import JsonObject

class TrafficParams(JsonObject):

    def __init__(self, json_struct=None):
        self.latency=0
        self.OSNR=""
        self.estimatedPLR=""
        self.qosClass=""
        self.reservedBandwidth=""
        super(TrafficParams, self).__init__(json_struct)

