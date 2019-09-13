#! /bin/bash

(cd tests/json; make)

# for file in tests/output/*; do
#
#    ext=${file##*.}
#
#    if [[ ${ext} = "json" ]]; then
#
#       target=$(basename -s .json "$file")
#
#       (cd tests/json/
#        echo "> cdblatex " ${target} "..."
#        cdblatex.sh -si ${target} &> ${target}.cdblog
#       )
#    fi
#
# done
