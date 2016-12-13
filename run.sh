#!/bin/bash

YANG="service-call service-topology"
JsonCodeTools="../JsonCodeTools/EAGLE-Open-Model-Profile-and-Tools/JsonCodeTools.py"
SWAGGER=""

for i in $YANG; do
  echo item: $i
  pyang -f swagger yang/$i.yang -o swagger/$i.json    
  OUT=${OUT:+$OUT }swagger/$i.json 
  echo $OUT
done
rm -rf cop-server/
python $JsonCodeTools $OUT -p=8081 -o cop-server/ 
