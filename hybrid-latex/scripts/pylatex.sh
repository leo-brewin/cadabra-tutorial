#!/bin/bash

file="<none>"
silent="no"
keep="no"
skiplatex="no"
Timer=""
Python="python"
sty=""
nowarn=""
mixed=""
reformat="yes"

# -----------------------------------------------------------------------------------------
# Parse the command-line options

OPTIND=1

while getopts 'i:I:P:sktTxhNM' option
do
   case "$option" in
   "i")  file="$OPTARG"           ;;
   "I")  sty="-I$OPTARG"          ;;
   "P")  Python="$OPTARG"         ;;
   "s")  silent="yes"             ;;
   "k")  keep="yes"               ;;
   "t")  Timer="/usr/bin/time"    ;;
   "T")  Timer="/usr/bin/time -l" ;;
   "x")  skiplatex="yes"          ;;
   "N")  nowarn="-N"              ;;
   "M")  mixed="-M"               ;;
   "X")  reformat="no"            ;;
   "h")  echo "usage : pylatex.sh -i file [-P<path to python>]"
         echo "                           [-I<path to pymacros.sty>] [-sktTxNMh]"
         echo "options :  -i file : source file (with or without .tex extension)"
         echo "           -I file : full path to pymacros.sty file"
         echo "           -P path : full path to the Python binary"
         echo "           -s : silent, don't open the pdf file"
         echo "           -k : keep all temporary files"
         echo "           -t : report brief cpu time"
         echo "           -T : report detailed cpu time plus memory usage"
         echo "           -x : don't call latex"
         echo "           -N : don't warn if errors found in the output for some tags"
         echo "           -M : source contains mixed sympy/symengine code"
         echo "           -X : do not reformat the .pytex output"
         echo "           -h : this help message"
         echo "example : pylatex.sh -i file -P/usr/local/bin/python"
         exit                ;;
   ?)    echo "pylatex.sh : Unknown option specified."
         exit                ;;
   esac
done

# strip .tex if given
file=$(basename -s ".tex" "$file")
name=$file

if [[ $file = "<none>" ]]; then
   echo "> no source file given, use pylatex.sh -i file"
   exit 1;
fi;

if [[ ! -e $file.tex ]]; then
   echo "> file ""$file.tex"" not found, exit"
   exit 1;
fi

# does the source contain \Input?
num=$(egrep -c -e'^\s*(\\|\@|\$)Input\{' "$file".tex)

# yes, now merge source files
if ! [[ $num = 0 ]]; then
   merge-src.py -i $file.tex -o .merged.tex
   name=".merged"
fi

touch $file.pytxt

pypreproc.py -i $file -m $name $mixed    || exit 1

$Timer $Python $file"_.py" > $file.pytxt || exit 3

pypostproc.py $nowarn -i $file $sty      || exit 5

# ----------------------------------------------------------
# optional: use SED to reformat the .pytex file
#
if [[ $reformat = "yes" ]]; then

   if [[ -e ${file}.pytex ]]; then

      # path to this script

      SCRIPT=$(readlink -f "$0")
      SEDSRC=${SCRIPT%.*}.sed

      SEDtext=/tmp/sedtext

      # combine global and local SED edits

      if [[ -e ${file}.sed ]]; then
         cat ${SEDSRC} ${file}.sed > ${SEDtext}
      else
         cat ${SEDSRC} > ${SEDtext}
      fi

      SED=/opt/homebrew/bin/gsed    # prefer a sed that understands extended regular expressions
      # SED=/usr/local/bin/sed        # this also works

      rm -rf ${file}.fail-reformat-pytex  # .fail-reformat exists only when an error occured

      pytex=${file}.pytex

      if [[ -e ${pytex} ]]; then

         rm -rf tmpA.del tmpB.del
         cp ${pytex} tmpA.del

         ${SED} -r -f ${SEDtext} tmpA.del > tmpB.del

         if ! [[ $? = 0 ]]; then
            touch ${file}.fail-reformat-pytex
            exit 9
         else
            mv tmpB.del ${pytex}
            rm -rf tmpA.del tmpB.del
         fi

      fi

   fi

fi

# ----------------------------------------------------------

if [[ $skiplatex = "no" ]]; then
   pdflatex -halt-on-error -interaction=batchmode -synctex=1 $file || exit 7
   echo " " # for some silly reason pdfsync forgets a trailing \n
else
   silent="yes"
fi

if [[ $silent = "no" ]]; then
   open $file.pdf       # macOS
   # xdg-open $file.pdf   # Linux
   # evince $file.pdf     # Linux
fi

if [[ $keep = "no" ]]; then
   rm -rf .merged.tex .tmp.txt
   rm -rf $file.log $file.out $file.py $file"_.py" $file.pyidx $file.pytxt
fi
