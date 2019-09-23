#-------------------------------------------------------------------------------
SHELL = /bin/bash
#-------------------------------------------------------------------------------
.PHONY: all tests
#-------------------------------------------------------------------------------
TARGETS = $(patsubst %.tex,%,$(wildcard example-[0-9][0-9]*.tex))
#-------------------------------------------------------------------------------
all:
	@ mkdir -p cdb pdf tests/output tests/expected
	@ for file in $(TARGETS); do make .$${file}; done;
	@ make examples
#-------------------------------------------------------------------------------
examples:
	@ make .examples
.examples: example-[0-9][0-9]*.pdf
	@ echo "pdflatex examples ..."
	@ pdflatex -halt-on-error -interaction=batchmode examples &> /dev/null
	@ cp -f examples.pdf pdf/.
	@ touch .examples
#-------------------------------------------------------------------------------
foo bah tmp:
	@ echo "cdblatex.sh $@ ..."
	@ cdblatex.sh -T -sx -i $@ &> $@.cdblog
	@ # echo " -->"`cdbstats -i $@.cdblog`
	@ pdflatex -halt-on-error -interaction=batchmode $@ &> /dev/null
	@ open $@.pdf
#-------------------------------------------------------------------------------
%:
	@ make .$*
.%:	%.tex
	@ echo "cdblatex.sh $* ..."
	@ cdblatex.sh -T -skx -i $* &> $*.cdblog
	@ # echo " -->"`cdbstats -i $*.cdblog`
	@ if [[ $* = example-06 ]]; then \
	     cdbcopy.py -i example-06 -t print.ex-06.02 -o example-06-1.cdbcopy; \
	     cdbcopy.py -i example-06 -t print.ex-06.04 -o example-06-2.cdbcopy; \
	     cdbcopy.py -i example-06 -t print.ex-06.05 -o example-06-3.cdbcopy; \
     fi
	@ pdflatex -halt-on-error -interaction=batchmode $* &> /dev/null
	@ pdflatex -halt-on-error -interaction=batchmode $* &> /dev/null
	@ # can't use wildcard with -e so test on one file
	@ cp -f $*.pdf    pdf/.
	@ cp -f $*.cdb    cdb/.
	@ cp -f $*.cdbtex tests/output/.
	@ if [[ -e $*-rab.c ]];     then cp -f $*-*.c tests/output/.;       fi
	@ if [[ -e $*-1.cdbcopy ]]; then cp -f $*-*.cdbcopy tests/output/.; fi
	@ if [[ -e $*.json ]];      then cp -f $*.json tests/output/.;      fi
	@ touch .$*
#-------------------------------------------------------------------------------
expected:
	@ cp -f tests/output/* tests/expected/.
	@ cp -f tests/semantic/output/* tests/semantic/expected/.
#-------------------------------------------------------------------------------
tests:
	@ tests.sh
#-------------------------------------------------------------------------------
rm-dot:
	@ for file in $(TARGETS); \
	  do \
	     rm -rf .$${file}; \
	  done
	@ rm -rf .[a-z]*.lb
	@ rm -rf .merged.tex .tmp.txt
	@ rm -rf .examples
#-------------------------------------------------------------------------------
rm-tests-output:
	@ rm -rf tests/output/*
	@ rm -rf tests/semantic/output/*
#-------------------------------------------------------------------------------
rm-output:
	@ rm -rf cdb/*
	@ rm -rf pdf/*
	@ rm -rf tests/output/*
	@ rm -rf tests/semantic/output/*
#-------------------------------------------------------------------------------
rm-expected:
	@ rm -rf tests/expected/*
	@ rm -rf tests/semantic/expected/*
#-------------------------------------------------------------------------------
clean:
	@ for file in $(TARGETS) examples; \
	  do \
	     rm -rf $${file}.aux $${file}.log $${file}.out $${file}.synctex.gz; \
	  done
#-------------------------------------------------------------------------------
veryclean:
	@ make clean
	@ for file in $(TARGETS); \
	  do \
		  rm -rf $${file}.pdf; \
		  rm -rf $${file}.cdb $${file}_.cdb; \
		  rm -rf $${file}.cdbidx $${file}.cdbtxt $${file}.cdblog; \
		  rm -rf $${file}.py; \
	  done
#-------------------------------------------------------------------------------
pristine:
	@ make rm-dot
	@ make rm-output
	@ make rm-expected
	@ make veryclean
	@ (cd tests/semantic; make pristine)
	@ for file in $(TARGETS) examples; \
	  do \
	     rm -rf $${file}.pdf; \
		  rm -rf $${file}.json $${file}*-*.c; \
		  rm -rf $${file}.cdbtex $${file}*-*.cdbcopy; \
	  done
#-------------------------------------------------------------------------------
# prepare files for github
github:
	@ make pristine
	@ make all
	@ make expected
	@ make rm-tests-output
	@ make rm-dot
	@ make veryclean
	@ rm -rf examples.pdf
	@ for file in $(TARGETS); \
	  do \
		  if [[ -e $${file}.json ]];      then mv -f $${file}.json      lib/.; fi ; \
		  if [[ -e $${file}.cdbtex ]];    then mv -f $${file}.cdbtex    lib/.; fi ; \
		  if [[ -e $${file}-rab.c ]];     then mv -f $${file}-*.c       lib/.; fi ; \
		  if [[ -e $${file}-1.cdbcopy ]]; then mv -f $${file}-*.cdbcopy lib/.; fi ; \
	  done
