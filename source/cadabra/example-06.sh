#! /bin/bash

echo "cdblatex.sh example-06 ..."
cdblatex.sh -T -skx -i example-06 &> example-06.cdblog
echo " -->"`cdbstats -i example-06.cdblog`
cdbcopy.py -i example-06 -t print.ex-06.02 -o example-06-1.cdbcopy
cdbcopy.py -i example-06 -t print.ex-06.04 -o example-06-2.cdbcopy
cdbcopy.py -i example-06 -t print.ex-06.05 -o example-06-3.cdbcopy
pdflatex -halt-on-error -interaction=batchmode example-06 &> /dev/null
# pdflatex -halt-on-error -interaction=batchmode example-06 &> /dev/null
open example-06.pdf
