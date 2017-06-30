from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS

import time
import thread

from funcs_cop_call.update_CallImpl import Update_CallImpl
from funcs_cop_call.remove_CallImpl import Remove_CallImpl
from funcs_cop_topology.update_TopologyImpl import Update_TopologyImpl
from funcs_cop_topology.remove_EdgeImpl import Remove_EdgeImpl
from funcs_cop_topology.remove_NodeImpl import Remove_NodeImpl
from funcs_cop_topology.add_EdgeImpl import Add_EdgeImpl
from funcs_cop_topology.add_EdgeendImpl import Add_EdgeendImpl
from funcs_cop_topology.add_NodeImpl import Add_NodeImpl
from funcs_cop_topology.remove_EdgeendImpl import Remove_EdgeendImpl
class BaseService:

    def __init__(self, proto):
        self.proto = proto

    def onOpen(self):
        pass


    def onClose(self, wasClean, code, reason):
        self.proto.sendClose(code=1000)

    def onMessage(self, payload, isBinary):
        pass


class UpdateCallService(BaseService):

    def onOpen(self):
        backend = Update_CallImpl(self.proto)
        backend.start()
        thread.start_new_thread(self.onAsyncronousEvent,(backend, 5))

    def onMessage(self, payload, isBinary):
        pass


    def onAsyncronousEvent(self, backend, timer):
        time.sleep(timer)
        backend.set_event(False)


class RemoveCallService(BaseService):

    def onOpen(self):
        backend = Remove_CallImpl(self.proto)
        backend.start()
        thread.start_new_thread(self.onAsyncronousEvent,(backend, 5))

    def onMessage(self, payload, isBinary):
        pass


    def onAsyncronousEvent(self, backend, timer):
        time.sleep(timer)
        backend.set_event(False)


class UpdateTopologyService(BaseService):

    def onOpen(self):
        backend = Update_TopologyImpl(self.proto)
        backend.start()
        thread.start_new_thread(self.onAsyncronousEvent,(backend, 5))

    def onMessage(self, payload, isBinary):
        pass


    def onAsyncronousEvent(self, backend, timer):
        time.sleep(timer)
        backend.set_event(False)


class RemoveEdgeService(BaseService):

    def onOpen(self):
        backend = Remove_EdgeImpl(self.proto)
        backend.start()
        thread.start_new_thread(self.onAsyncronousEvent,(backend, 5))

    def onMessage(self, payload, isBinary):
        pass


    def onAsyncronousEvent(self, backend, timer):
        time.sleep(timer)
        backend.set_event(False)


class RemoveNodeService(BaseService):

    def onOpen(self):
        backend = Remove_NodeImpl(self.proto)
        backend.start()
        thread.start_new_thread(self.onAsyncronousEvent,(backend, 5))

    def onMessage(self, payload, isBinary):
        pass


    def onAsyncronousEvent(self, backend, timer):
        time.sleep(timer)
        backend.set_event(False)


class AddEdgeService(BaseService):

    def onOpen(self):
        backend = Add_EdgeImpl(self.proto)
        backend.start()
        thread.start_new_thread(self.onAsyncronousEvent,(backend, 5))

    def onMessage(self, payload, isBinary):
        pass


    def onAsyncronousEvent(self, backend, timer):
        time.sleep(timer)
        backend.set_event(False)


class AddEdgeEndService(BaseService):

    def onOpen(self):
        backend = Add_EdgeendImpl(self.proto)
        backend.start()
        thread.start_new_thread(self.onAsyncronousEvent,(backend, 5))

    def onMessage(self, payload, isBinary):
        pass


    def onAsyncronousEvent(self, backend, timer):
        time.sleep(timer)
        backend.set_event(False)


class AddNodeService(BaseService):

    def onOpen(self):
        backend = Add_NodeImpl(self.proto)
        backend.start()
        thread.start_new_thread(self.onAsyncronousEvent,(backend, 5))

    def onMessage(self, payload, isBinary):
        pass


    def onAsyncronousEvent(self, backend, timer):
        time.sleep(timer)
        backend.set_event(False)


class RemoveEdgeEndService(BaseService):

    def onOpen(self):
        backend = Remove_EdgeendImpl(self.proto)
        backend.start()
        thread.start_new_thread(self.onAsyncronousEvent,(backend, 5))

    def onMessage(self, payload, isBinary):
        pass


    def onAsyncronousEvent(self, backend, timer):
        time.sleep(timer)
        backend.set_event(False)


class ServiceServerProtocol(WebSocketServerProtocol):

    SERVICEMAP = { '/restconf/streams/removeNodeService' : RemoveNodeService, '/restconf/streams/updateCallService' : UpdateCallService, '/restconf/streams/addNodeService' : AddNodeService, '/restconf/streams/updateTopologyService' : UpdateTopologyService, '/restconf/streams/removeEdgeEndService' : RemoveEdgeEndService, '/restconf/streams/addEdgeService' : AddEdgeService, '/restconf/streams/removeEdgeService' : RemoveEdgeService, '/restconf/streams/addEdgeEndService' : AddEdgeEndService, '/restconf/streams/removeCallService' : RemoveCallService }

    def __init__(self):
        super(ServiceServerProtocol, self).__init__()
        self.service = None

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        if request.path in self.SERVICEMAP:
            cls = self.SERVICEMAP[request.path]
            self.service = cls(self)
        else:
            err = "No service under %s" % request.path
            print(err)

    def onOpen(self):
        if self.service:
            self.service.onOpen()

    def onMessage(self, payload, isBinary):
        if self.service:
            self.service.onMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        if self.service:
            self.service.onClose(wasClean, code, reason)


class NotificationServerFactory():

    def __init__(self):
        print '\nRunning notification server in port 8181'
        factory = WebSocketServerFactory('ws://localhost:8181')
        factory.protocol = ServiceServerProtocol
        listenWS(factory)
        try:
            reactor.run(installSignalHandlers=0)
        except KeyboardInterrupt:
            reactor.stop()