#!/bin/bash

# defaults, edit to suit

if [[ $HERE = '' ]]; then
   HERE=$HOME/local/cadabra-tutorial/
fi;

MyBin=$HERE/bin/
MyLib=$HERE/lib/
MyTex=$HERE/tex/

# Parse the command-line options

while getopts 'b:l:t:h' option
do
   case "$option" in
   "b")  MyBin="$OPTARG"      ;;
   "l")  MyLib="$OPTARG"      ;;
   "t")  MyTex="$OPTARG"      ;;
   "h")  echo "usage : INSTALL.sh [-bBIN] [-lLIB] [-tTEX]"
         echo "options : -b : where to find the binaries and shell scripts"
         echo "          -l : where to find the python libraries"
         echo "          -t : where to find the LaTeX files "
         echo "          -h : this help message"
         exit                 ;;
   ?)    echo "INSTALL.sh: Unknown option specified."
         exit                 ;;
   esac
done

mkdir -p $MyBin $MyLib $MyTex

(cd hybrid-latex; INSTALL.sh -b $MyBin -l $MyLib -t $MyTex)
