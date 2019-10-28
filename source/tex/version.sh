#! /bin/bash

version=$(egrep -o "Cadabra 2.+[0-9]\)" $HOME/Cadabra/v2.0/core/cadabra2)

echo "\def\CdbVersion{"$version"}" > version.tex
