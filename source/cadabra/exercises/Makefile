#-------------------------------------------------------------------------------
SHELL = /bin/bash
#-------------------------------------------------------------------------------
.PHONY: all tests
#-------------------------------------------------------------------------------
TARGETS = $(patsubst %.tex,%,$(wildcard ex-[0-9][0-9][0-9][0-9]*.tex))
#-------------------------------------------------------------------------------
all:
	@ mkdir -p cdb pdf tests/output tests/expected
	@ for file in $(TARGETS); do make .$${file}; done;
	@ make exercises
#-------------------------------------------------------------------------------
exercises:
	@ make .exercises
.exercises: ex-[0-9][0-9][0-9][0-9]*.pdf
	@ echo "pdflatex exercises ..."
	@ pdflatex -halt-on-error -interaction=batchmode exercises &> /dev/null
	@ cp -f exercises.pdf pdf/.
	@ touch .exercises
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
	@ if [[ $* = ex-0107 ]]; then \
	     cdbcopy.py -i ex-0107 -t print.0107 -o ex-0107.cdbcopy; \
     fi
	@ if [[ $* = ex-0605 ]]; then \
	     cdbcopy.py -i ex-0605 -t print.0605 -o ex-0605.cdbcopy; \
     fi
	@ if [[ $* = ex-0606 ]]; then \
	     cdbcopy.py -i ex-0606 -t print.0606 -o ex-0606.cdbcopy; \
     fi
	@ pdflatex -halt-on-error -interaction=batchmode $* &> /dev/null
	@ pdflatex -halt-on-error -interaction=batchmode $* &> /dev/null
	@ cp -f $*.pdf pdf/.
	@ cp -f $*.cdb cdb/.
	@ cp -f $*.cdbtex tests/output/.
	@ if [[ -e $*.c    ]]; then cp -f $*.c    tests/output/.; fi
	@ if [[ -e $*.json ]]; then cp -f $*.json tests/output/.; fi
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
#-------------------------------------------------------------------------------
rm-output:
	@ rm -rf cdb/*
	@ rm -rf pdf/*
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
	@ for file in $(TARGETS) exercises; \
	  do \
	     rm -rf $${file}.pdf $${file}.txt; \
		  rm -rf $${file}.json $${file}*.c; \
		  rm -rf $${file}.cdbtex $${file}.cdbcopy; \
	  done
#-------------------------------------------------------------------------------
# prepare files for github
github:
	@ make pristine
	@ make all
	@ (rm -rf tmppdf; cp -rf pdf tmppdf)
	@ (rm -rf tmpcdb; cp -rf cdb tmpcdb)
	@ make expected
	@ make rm-dot
	@ make rm-output
	@ make veryclean
	@ for file in $(TARGETS) exercises; \
	  do \
	     rm -rf $${file}.pdf $${file}.txt; \
		  rm -rf $${file}.json $${file}*.c; \
		  rm -rf $${file}.cdbtex $${file}.cdbcopy; \
	  done
	@ (rm -rf pdf; mv tmppdf pdf)
	@ (rm -rf cdb; mv tmpcdb cdb)
