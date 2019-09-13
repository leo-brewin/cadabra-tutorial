#!/bin/bash

export CADABRA_NO_UNICODE=1
export PYTHONWARNINGS="ignore"

file="<none>"
silent="no"
keep="no"
skiplatex="no"
Timer=""
CDB=/usr/local/bin/
sty=""
warn=""

# -----------------------------------------------------------------------------------------
# Parse the command-line options

OPTIND=1

while getopts 'i:I:P:sktTxhW' option
do
   case "$option" in
   "i")  file="$OPTARG"      ;;
   "I")  sty="-I$OPTARG"     ;;
   "P")  CDB="$OPTARG"       ;;
   "s")  silent="yes"        ;;
   "k")  keep="yes"          ;;
   "t")  Timer="/usr/bin/time" ;;
   "T")  Timer="/usr/bin/time -l" ;;
   "x")  skiplatex="yes"     ;;
   "W")  warn="-W"           ;;
   "h")  echo "usage : cdblatex.sh -i file [-P<path to Cadabra bin dir>] [-I<path to cdbmacros.sty>] [-s] [-k] [-x] [-h]"
         echo "options :  -i file : source file (with or without .tex extension)"
         echo "           -I file : full path to cdbmacros.sty file"
         echo "           -P file : path to Cadabra bin directory"
         echo "           -s : silent, don't open the pdf file"
         echo "           -k : keep all temporary files"
         echo "           -t : report brief cpu time"
         echo "           -T : report detailed cpu time plus memory usage"
         echo "           -x : don't call latex"
         echo "           -h : this help messag"
         echo "           -W : warn if errors found in the output for some tags"
         echo "example : cdblatex.sh -i file"
         exit                ;;
   ?)    echo "cdblatex.sh : Unknown option specified."
         exit                ;;
   esac
done

# strip .tex if given
file=$(basename -s ".tex" "$file")
name=$file

if [[ $file = "<none>" ]]; then
   echo "> no source file given, use cdblatex.sh -i file"
   exit 1;
fi;

if [[ ! -e $file.tex ]]; then
   echo "> file ""$file.tex"" not found, exit"
   exit 1;
fi

# does the source contain \Input?
num=$(egrep -c -e'^\s*\\Input\{' "$file".tex)

# yes, now merge source files
if ! [[ $num = 0 ]]; then
   merge-tex.py -i $file.tex -o .merged.tex
   name=".merged"
fi

touch $file.cdbtxt

cdbpreproc.py -i $file -m $name            || exit 1

$CDB/cadabra2python $file"_.cdb" $file.py  || exit 3

$Timer $CDB/cadabra2 $file.py > .tmp.txt   || exit 5

iconv -c -f UTF-8 -t ASCII//translit .tmp.txt > $file.cdbtxt

# ---------------------------------------------------------
# LCB: this problem fixed in ~/local/lib/python/cdblib.py
#
# export of rules will use unicode character for '->' and this
# causes problems later when those rules are imported by other codes
# if [[ -e $file.json ]]; then
#    cp $file.json .tmp.json
#    iconv -c -f UTF-8 -t ASCII//translit .tmp.json > $file.json
#    rm -rf .tmp.json
# fi
# ---------------------------------------------------------

cdbpostproc.py $warn -i $file $sty       || exit 7

if [[ $skiplatex = "no" ]]; then
   pdflatex -halt-on-error -interaction=batchmode -synctex=1 $file || exit 9
   echo " " # for some silly reason pdfsync forgets a trailing \n
else
   silent="yes"
fi

if [[ $silent = "no" ]]; then
   open $file.pdf       # macOS
   # xdg-open $file.pdf   # Linux
   # evince $file.pdf     # Linux
fi

rm -rf comment.cut .tmp.txt

if [[ $keep = "no" ]]; then
   rm -rf comment.cut
   rm -rf .merged.tex .tmp.txt
   rm -rf $file.log $file.out $file.py $file"_.cdb" $file.cdbidx $file.cdbtxt
fi
