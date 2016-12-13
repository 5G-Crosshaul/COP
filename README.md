# CONTROL ORCHESTRATION PROTOCOL (COP)

## Overview
The Control Orchestration Procotol (COP) abstracts a set of control plane functions used by an SDN Controller, allowing the interworking of heterogenous control plane paradigms (i.e., OpenFlow, GMPLS/PCE).

The COP is defined using YANG models and RESTCONF. We provide the [YANG models](COP/tree/master/yang) and a set of tools to process the YANG models and obtain the necessary classes and interfaces that will support the COP. These tools are contributed in [OpenSourceSDN.org EAGLE](https://github.com/OpenNetworkingFoundation/EAGLE-Open-Model-Profile-and-Tools). Please check the following branches:

- [YangJsonTools](https://github.com/OpenNetworkingFoundation/EAGLE-Open-Model-Profile-and-Tools/tree/YangJsonTools)
- [JsonCodeTools](https://github.com/OpenNetworkingFoundation/EAGLE-Open-Model-Profile-and-Tools/tree/JsonCodeTools)

## COP YANG models

The [COP YANG models](COP/tree/master/yang) are available for discussion to research community. Up to now three YANG models have been discussed:

- [service-call.yang](yang/service-call.yang)
- [service-topology.yang](yang/service-topology.yang)
- [service-path-computation.yang](yang/service-path-computation.yang)


License
-------
The COP has been forked from [FP7 STRAUSS project](http://www.ict-strauss.eu/) project. 
It is currently being used, updated and mantained by [H2020 5G-Crosshaul project](http://5g-crosshaul.eu/). 
