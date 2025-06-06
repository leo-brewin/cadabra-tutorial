#-------------------------------------------------------------------------------
SHELL = /bin/bash
#-------------------------------------------------------------------------------
.PHONY: all tests
#-------------------------------------------------------------------------------
TARGETS = dgeom $(patsubst %.tex,%,$(wildcard example-[0-9][0-9]*.tex))
#-------------------------------------------------------------------------------
all:
	@ mkdir -p cdb pdf lib
	@ mkdir -p tests/output tests/expected
	@ mkdir -p tests/semantic/output tests/semantic/expected
	@ for file in $(TARGETS); do make .$${file}; done;
	@ make examples
#-------------------------------------------------------------------------------
examples:
	@ make .examples
.examples: example-[0-9][0-9]*.tex
	@ echo "pdflatex examples ..."
	@ pdflatex -halt-on-error -interaction=batchmode examples &> /dev/null
	@ if [[ -e examples.pdf ]]; then \
	      cp -f examples.pdf pdf/.; \
	      cp -f examples.pdf ../../pdf/.; \
			touch .examples; \
	  fi
#-------------------------------------------------------------------------------
%:
	@ make .$*
.%:	%.tex
	@ echo "cdblatex.sh $* ..."
	@ cdblatex.sh -T -skx -i $* &> $*.cdblog
	@ # echo " -->"`cputime -i $*.cdblog`
	@ if [[ $* = example-06 ]]; then \
	     cdbcopy.py -i example-06 -t print.ex-06.04 -o example-06-04.cdbcopy; \
	     cdbcopy.py -i example-06 -t print.ex-06.05 -o example-06-05.cdbcopy; \
     fi
	@ pdflatex -halt-on-error -interaction=batchmode $* &> /dev/null
	@ pdflatex -halt-on-error -interaction=batchmode $* &> /dev/null
	@ # can't use wildcard with -e so test on one file
	@ cp -f $*.pdf    pdf/.
	@ cp -f $*.cdb    cdb/.
	@ cp -f $*.cdbtex lib/.
	@ cp -f $*.cdbtex tests/output/.
	@ if [[ -e $*-rab.c ]];      then cp -f $*-*.c       tests/output/.; fi
	@ if [[ -e $*-04.cdbcopy ]]; then cp -f $*-*.cdbcopy tests/output/.; fi
	@ if [[ -e $*.json ]];       then cp -f $*.json      tests/output/.; fi
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
rm-output:
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
	@ for file in $(TARGETS) examples; \
	  do \
		  rm -rf $${file}.pdf; \
		  rm -rf $${file}.cdb $${file}_.cdb $${file}_.txt; \
		  rm -rf $${file}.cdbidx $${file}.cdbtxt $${file}.cdblog; \
		  rm -rf $${file}.py; \
	  done
#-------------------------------------------------------------------------------
pristine:
	@ make rm-dot
	@ make rm-output
	@ make rm-expected
	@ make veryclean
	@ rm -rf cdb/* lib/* pdf/*
	@ (cd tests/semantic; make pristine)
	@ for file in $(TARGETS) examples; \
	  do \
	     rm -rf $${file}.pdf; \
		  rm -rf $${file}.json $${file}*-*.c; \
		  rm -rf $${file}.cdbtex $${file}*-*.cdbcopy; \
	  done
#-------------------------------------------------------------------------------
github-clean:
	@ make rm-dot
	@ make rm-output
	@ make veryclean
	@ for file in $(TARGETS) examples; \
	  do \
		  if [[ -e $${file}.cdbtex ]];     then rm -f $${file}.cdbtex; fi ; \
		  if [[ -e $${file}.json ]];       then mv -f $${file}.json      lib/.; fi ; \
		  if [[ -e $${file}-rab.c ]];      then mv -f $${file}-*.c       lib/.; fi ; \
		  if [[ -e $${file}-04.cdbcopy ]]; then mv -f $${file}-*.cdbcopy lib/.; fi ; \
	  done
#-------------------------------------------------------------------------------
# prepare files for github
github:
	@ make pristine
	@ make all
	@ make expected
	@ make github-clean
