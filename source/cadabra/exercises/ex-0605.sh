#! /bin/bash

echo "cdblatex.sh ex-0605 ..."
cdblatex.sh -T -skx -i ex-0605 &> ex-0605.cdblog
echo " -->"`cdbstats -i ex-0605.cdblog`
cdbcopy.py -i ex-0605 -t print.0605 -o ex-0605.cdbcopy
pdflatex -halt-on-error -interaction=batchmode ex-0605 &> /dev/null
# pdflatex -halt-on-error -interaction=batchmode ex-0605 &> /dev/null
open ex-0605.pdf
