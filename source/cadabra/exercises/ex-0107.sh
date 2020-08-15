#! /bin/bash

echo "cdblatex.sh ex-0107 ..."
cdblatex.sh -T -skx -i ex-0107 &> ex-0107.cdblog
# echo " -->"`cputime -i ex-0107.cdblog`
cdbcopy.py -i ex-0107 -t print.0107 -o ex-0107.cdbcopy
pdflatex -halt-on-error -interaction=batchmode ex-0107 &> /dev/null
# pdflatex -halt-on-error -interaction=batchmode ex-0107 &> /dev/null
open ex-0107.pdf
