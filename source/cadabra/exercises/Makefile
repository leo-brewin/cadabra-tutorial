#-------------------------------------------------------------------------------
SHELL = /bin/bash
#-------------------------------------------------------------------------------
.PHONY: all tests
#-------------------------------------------------------------------------------
TARGETS = $(patsubst %.tex,%,$(wildcard ex-[0-9][0-9][0-9][0-9]*.tex))
#-------------------------------------------------------------------------------
all:
	@ mkdir -p cdb pdf lib
	@ mkdir -p tests/output tests/expected
	@ for file in $(TARGETS); do make .$${file}; done;
	@ make exercises
#-------------------------------------------------------------------------------
exercises:
	@ make .exercises
.exercises: ex-[0-9][0-9][0-9][0-9]*.tex
	@ echo "pdflatex exercises ..."
	@ pdflatex -halt-on-error -interaction=batchmode exercises &> /dev/null
	@ if [[ -e exercises.pdf ]]; then \
	      cp -f exercises.pdf pdf/.; \
	      cp -f exercises.pdf ../../../pdf/.; \
			touch .exercises; \
	  fi
#-------------------------------------------------------------------------------
%:
	@ make .$*
.%:	%.tex
	@ echo "cdblatex.sh $* ..."
	@ cdblatex.sh -T -skx -i $* &> $*.cdblog
	@ # echo " -->"`cputime -i $*.cdblog`
	@ if [[ $* = ex-0107 ]]; then \
	     cdbcopy.py -i ex-0107 -t print.0107 -o ex-0107.cdbcopy; \
     fi
	@ pdflatex -halt-on-error -interaction=batchmode $* &> /dev/null
	@ pdflatex -halt-on-error -interaction=batchmode $* &> /dev/null
	@ cp -f $*.pdf    pdf/.
	@ cp -f $*.cdb    cdb/.
	@ cp -f $*.cdbtex lib/.
	@ cp -f $*.cdbtex tests/output/.
	@ if [[ -e $*.c       ]]; then cp -f $*.c       tests/output/.; fi
	@ if [[ -e $*.json    ]]; then cp -f $*.json    tests/output/.; fi
	@ if [[ -e $*.cdbcopy ]]; then cp -f $*.cdbcopy tests/output/.; fi
	@ touch .$*
#-------------------------------------------------------------------------------
expected:
	@ cp -f tests/output/* tests/expected/.
#-------------------------------------------------------------------------------
tests:
	@ tests.sh
#-------------------------------------------------------------------------------
rm-dot:
	@ for file in $(TARGETS) exercises; \
	  do \
	     rm -rf .$${file}; \
	  done
	@ rm -rf .[a-z]*.lb
	@ rm -rf .merged.tex .tmp.txt
#-------------------------------------------------------------------------------
rm-output:
	@ rm -rf tests/output/*
#-------------------------------------------------------------------------------
rm-expected:
	@ rm -rf tests/expected/*
#-------------------------------------------------------------------------------
clean:
	@ for file in $(TARGETS) exercises; \
	  do \
	     rm -rf $${file}.aux $${file}.log $${file}.out $${file}.synctex.gz; \
	  done
#-------------------------------------------------------------------------------
veryclean:
	@ make clean
	@ for file in $(TARGETS) exercises; \
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
	@ rm -rf cdb/* lib/* pdf/*
	@ for file in $(TARGETS) exercises; \
	  do \
	     rm -rf $${file}.pdf $${file}.txt; \
		  rm -rf $${file}.json $${file}*.c; \
		  rm -rf $${file}.cdbtex $${file}.cdbcopy; \
	  done
#-------------------------------------------------------------------------------
github-clean:
	@ make rm-dot
	@ make rm-output
	@ make veryclean
	@ for file in $(TARGETS) exercises; \
	  do \
		  if [[ -e $${file}.cdbtex ]];  then rm -f $${file}.cdbtex; fi ; \
		  if [[ -e $${file}.json ]];    then mv -f $${file}.json    lib/.; fi ; \
		  if [[ -e $${file}-rab.c ]];   then mv -f $${file}*.c      lib/.; fi ; \
		  if [[ -e $${file}.cdbcopy ]]; then mv -f $${file}.cdbcopy lib/.; fi ; \
	  done
#-------------------------------------------------------------------------------
# prepare files for github
github:
	@ make pristine
	@ make all
	@ make expected
	@ make github-clean
