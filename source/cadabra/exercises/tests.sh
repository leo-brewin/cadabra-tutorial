#! /bin/bash

for file in tests/output/*; do

   target=$(basename "$file")

   echo "> diff" ${target}
   diff tests/expected/${target} tests/output/${target}

done
