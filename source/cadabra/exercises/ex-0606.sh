#! /bin/bash

echo "cdblatex.sh ex-0606 ..."
cdblatex.sh -T -skx -i ex-0606 &> ex-0606.cdblog
echo " -->"`cdbstats -i ex-0606.cdblog`
cdbcopy.py -i ex-0606 -t print.0606 -o ex-0606.cdbcopy
pdflatex -halt-on-error -interaction=batchmode ex-0606 &> /dev/null
# pdflatex -halt-on-error -interaction=batchmode ex-0606 &> /dev/null
open ex-0606.pdf
