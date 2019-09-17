#-------------------------------------------------------------------------------
SHELL = /bin/bash
#-------------------------------------------------------------------------------
.PHONY: all pdf tests
#-------------------------------------------------------------------------------
TARGETS = $(patsubst %.tex,%,$(wildcard ex-[0-9][0-9][0-9][0-9]*.tex))
#-------------------------------------------------------------------------------
all:
	@ mkdir -p pdf cdb tests/output tests/expected
	@ for file in $(TARGETS); do make .$${file}; done;
	@ make exercises
#-------------------------------------------------------------------------------
pdf:
	@ mkdir -p pdf
	@ for file in $(TARGETS); do make $${file}.pdf; done;
#-------------------------------------------------------------------------------
exercises:
	@ make .exercises
.exercises: ex-[0-9][0-9][0-9][0-9]*.pdf
	@ echo "pdflatex exercises ..."
	@ pdflatex -halt-on-error -interaction=batchmode exercises &> exercises.log
	@ touch .exercises
#-------------------------------------------------------------------------------
foo bah tmp:
	@ echo "cdblatex.sh $@ ..."
	@ cdblatex.sh -T -sx -i $@ &> $@.cdblog
	@ # echo " -->"`cdbstats -i $@.cdblog`
	@ pdflatex -halt-on-error -interaction=batchmode $@ &> $@.cdblog
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
	@ pdflatex -halt-on-error -interaction=batchmode $* &> $*.cdblog
	@ cp -f $*.cdb cdb/.
	@ cp -f $*.cdbtex tests/output/.
	@ if [[ -e $*.c    ]]; then cp -f $*.c    tests/output/.; fi
	@ if [[ -e $*.json ]]; then cp -f $*.json tests/output/.; fi
	@ touch .$*
#-------------------------------------------------------------------------------
%.pdf: %.tex
	@ echo "pdflatex $* ..."
	@ pdflatex -halt-on-error -interaction=batchmode $* &> /dev/null || exit 1
	@ cp -f $*.pdf pdf/.
#-------------------------------------------------------------------------------
expected:
	@ for file in $(TARGETS); \
	  do \
	     cp -f $${file}.pdf pdf/.; \
	  done
	@ cp -f tests/output/* tests/expected/.
	@ cp -f exercises.pdf pdf/.
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
	@ rm -rf pdf/*.pdf
	@ rm -rf tests/output/*.c
	@ rm -rf tests/output/*.json
	@ rm -rf tests/output/*.*tex
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
		  rm -rf $${file}.cdb $${file}_.cdb $${file}.cdbidx $${file}.cdbtxt $${file}.cdblog $${file}*.cdbcopy; \
		  rm -rf $${file}.py $${file}.pytxt $${file}.pylog; \
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
		  rm -rf $${file}.pytex $${file}.cdbtex; \
	  done
#-------------------------------------------------------------------------------
# prepare files for github
github:
	@ make pristine
	@ make all
	@ make expected
	@ make veryclean
	@ make rm-output
