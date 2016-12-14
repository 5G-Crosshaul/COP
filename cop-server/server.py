from flask import Flask
import thread
from notification_factory import NotificationServerFactory
## EXAMPLE IMPORT SERVER MODELS
import cop_call
import cop_topology
import backend_api

def launch_notification_server():
    return thread.start_new_thread(NotificationServerFactory,())



app = Flask(__name__)
app.register_blueprint(getattr(cop_call, "cop_call"))
app.register_blueprint(getattr(cop_topology, "cop_topology"))
app.register_blueprint(getattr(backend_api, 'backend_api'))

if __name__ == "__main__":
    nf = launch_notification_server()
    app.run(host='0.0.0.0', port = 8081, debug=True)
    