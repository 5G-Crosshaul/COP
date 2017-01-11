#!/bin/bash

YANG="cop-call cop-topology"
JsonCodeTools="../JsonCodeTools/EAGLE-Open-Model-Profile-and-Tools/JsonCodeTools.py"
SWAGGER=""


for i in $YANG; do
  echo item: $i
  cd yang
  pyang -f swagger $i.yang -o ../swagger/$i.json
  pyang -f uml $i.yang -o ../$i.uml
  cd ..
  java -jar plantuml.jar $i.uml        
  OUT=${OUT:+$OUT }swagger/$i.json 
  echo $OUT
done
python $JsonCodeTools $OUT -p=8081 -o cop-server/ 
