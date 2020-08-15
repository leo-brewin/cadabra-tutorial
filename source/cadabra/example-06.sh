#! /bin/bash

echo "cdblatex.sh example-06 ..."
cdblatex.sh -T -skx -i example-06 &> example-06.cdblog
# echo " -->"`cputime -i example-06.cdblog`
cp example-06.cdbtex lib/.
cdbcopy.py -i example-06 -t print.ex-06.04 -o example-06-04.cdbcopy
cdbcopy.py -i example-06 -t print.ex-06.05 -o example-06-05.cdbcopy
pdflatex -halt-on-error -interaction=batchmode example-06 &> /dev/null
# pdflatex -halt-on-error -interaction=batchmode example-06 &> /dev/null
open example-06.pdf
