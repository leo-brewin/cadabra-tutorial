#! /bin/bash

echo "---------------------------------------------------------"
echo "  diff *.c"
tests-c.sh

echo "---------------------------------------------------------"
echo "  diff *.cdbtex"
tests-cdbtex.sh

echo "---------------------------------------------------------"
echo "  diff *.cdbtex"
tests-cdbcopy.sh

echo "---------------------------------------------------------"
echo "  checking *.json files, results in tests/json/gallery.pdf"
tests-json.sh
