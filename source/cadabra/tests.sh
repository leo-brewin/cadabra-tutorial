#! /bin/bash

echo "---------------------------------------------------------"
echo "  diff *.c"
tests-c.sh

echo "---------------------------------------------------------"
echo "  diff *.cdbtex"
tests-cdbtex.sh

echo "---------------------------------------------------------"
echo "  diff *.cdbcopy"
tests-cdbcopy.sh

echo "---------------------------------------------------------"
echo "  checkpoint files, results in tests/semantic/summary.pdf"
tests-semantic.sh
