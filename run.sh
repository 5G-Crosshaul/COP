#!/bin/bash

YANG="service-call service-topology"
JsonCodeTools="../JsonCodeTools/EAGLE-Open-Model-Profile-and-Tools/JsonCodeTools.py"

for i in $YANG; do
  echo item: $i
  pyang -f swagger yang/$i.yang -o swagger/$i.json
  rm -rf cop-server/
  python $JsonCodeTools swagger/$i.json -p=8081 -o cop-server/ 
done
