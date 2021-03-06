#! /bin/bash

for file in tests/output/*; do

   ext=${file##*.}

   target=$(basename "$file")

   if [[ ${ext} = "cdbcopy" ]]; then
      echo "> diff" ${target}
      diff tests/output/${target} tests/expected/${target}
   fi

done
