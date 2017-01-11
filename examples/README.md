# COP usage examples

## Request context

curl -X GET -H "Content-type:application/json" -u admin:pswd1 http://localhost:8081/restconf/config/context/

## Create a Service Call

curl -X POST -H "Content-type:application/json" -u admin:pswd1 http://localhost:8081/restconf/config/calls/call/call_1/ -d '{"callId":"call_1","aEnd":{"nodeId":"10.0.50.1","edgeEndId":"1","endpointId":"ep1"}, "zEnd":{"nodeId":"10.0.50.2","edgeEndId":"2","endpointId":"ep2"}, "trafficParams":{"latency":100,"reservedBandwidth":100000000},"transportLayer":{"layer":"ethernet", "direction":"bidir"}}'

## Get Call information

curl -X GET -H "Content-type:application/json" -u admin:pswd1 http://localhost:8081/restconf/config/calls/

## Notifications

### OSNR

### PLR (Packet Loss Ratio)
