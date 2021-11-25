#! /bin/bash

# version="Cadabra 2.3.7 (build 2778.b0ba2dbb80 dated 2021-09-27)"

if [[ -x /usr/local/bin/cadabra2 ]]; then
   version=$(/usr/local/bin/cadabra2 < /dev/null 2>/dev/null | grep -oE -e "Cadabra 2.+[0-9]\)")
else
   version="Cadabra: unknown version"
fi

echo "\def\CdbVersion{"$version"}" > version.tex
