import os.path, sys
import threading
import json
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__))))

from objects_cop_topology.topology import Topology


class Update_TopologyImpl (threading.Thread):
    def __init__(self, handler):
        threading.Thread.__init__(self)
        self.event = True
        self.handler = handler

    def set_event(self, event):
        print 'Event received'
        self.event = event

    def run(self):
        while self.event:
            time.sleep(1)

        payload = json.dumps(Topology({"callId":"Example_Update_Topology"}).json_serializer()).encode('utf8')
        self.handler.sendMessage(payload, False)