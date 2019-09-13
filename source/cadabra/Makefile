#-------------------------------------------------------------------------------
SHELL = /bin/bash
SED   = /usr/local/bin/sed
#-------------------------------------------------------------------------------
.PHONY: all pdf tests
#-------------------------------------------------------------------------------
TARGETS = $(patsubst %.tex,%,$(wildcard example-[0-9][0-9]*.tex))
#-------------------------------------------------------------------------------
all:
	@ mkdir -p cdb pdf tests/output tests/expected
	@ for file in $(TARGETS); do make .$${file}; done;
	@ make examples
#-------------------------------------------------------------------------------
pdf:
	@ mkdir -p pdf
	@ for file in $(TARGETS); do make $${file}.pdf; done;
#-------------------------------------------------------------------------------
examples:
	@ make .examples
.examples: example-[0-9][0-9]*.pdf
	@ echo "pdflatex examples ..."
	@ pdflatex -halt-on-error -interaction=batchmode examples &> examples.log
	@ touch .examples
#-------------------------------------------------------------------------------
foo bah tmp:
	@ echo "cdblatex.sh $@ ..."
	@ cdblatex.sh -T -sx -i $@ &> $@.cdblog
	@ $(SED) -e 's!\\,_!\{\}_!g' $@.cdbtex > tmp.del; if [[ $$? = 0 ]]; then cp -f tmp.del $@.cdbtex; else exit 3; fi; rm -rf tmp.del
	@ $(SED) -e 's!\\,^!\{\}^!g' $@.cdbtex > tmp.del; if [[ $$? = 0 ]]; then cp -f tmp.del $@.cdbtex; else exit 3; fi; rm -rf tmp.del
	@ echo " -->"`cdbstats -i $@.cdblog`
	@ pdflatex -halt-on-error -interaction=batchmode $@ &> $@.cdblog
	@ open $@.pdf
#-------------------------------------------------------------------------------
%:
	@ make .$*
.%:	%.tex
	@ echo "cdblatex.sh $* ..."
	@ cdblatex.sh -T -skx -i $* &> $*.cdblog
	@ $(SED) -e 's!\\,_!\{\}_!g' $*.cdbtex > tmp.del; if [[ $$? = 0 ]]; then cp -f tmp.del $*.cdbtex; else exit 3; fi; rm -rf tmp.del
	@ $(SED) -e 's!\\,^!\{\}^!g' $*.cdbtex > tmp.del; if [[ $$? = 0 ]]; then cp -f tmp.del $*.cdbtex; else exit 3; fi; rm -rf tmp.del
	@ echo " -->"`cdbstats -i $*.cdblog`
	@ cp -f $*.cdb cdb/.
	@ cp -f $*.cdbtex tests/output/.
	@ if [[ $* = example-06 ]]; then \
	     cdbcopy.py -i example-06 -t print.ex-06.02 -o example-06-1.cdbcopy; \
	     cdbcopy.py -i example-06 -t print.ex-06.04 -o example-06-2.cdbcopy; \
	     cdbcopy.py -i example-06 -t print.ex-06.05 -o example-06-3.cdbcopy; \
     fi
	@ pdflatex -halt-on-error -interaction=batchmode $* &> $*.cdblog
	@ # can't use wildcard with -e so test on one file
	@ if [[ -e $*-rab.c ]]; then cp -f $*-*.c tests/output/.; fi
	@ if [[ -e $*-1.cdbcopy ]]; then cp -f $*-*.cdbcopy tests/output/.; fi
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
	@ cp -f examples.pdf pdf/.
#-------------------------------------------------------------------------------
tests:
	@ tests.sh
#-------------------------------------------------------------------------------
rm-dot:
	@ for file in $(TARGETS) examples; \
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
	@ rm -rf tests/output/*.*cdbcopy
#-------------------------------------------------------------------------------
rm-expected:
	@ rm -rf tests/expected/*
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
		  rm -rf $${file}.cdb $${file}_.cdb; \
		  rm -rf $${file}.cdbidx $${file}.cdbtxt $${file}.cdblog; \
		  rm -rf $${file}.py $${file}.pytxt $${file}.pylog; \
	  done
#-------------------------------------------------------------------------------
pristine:
	@ make rm-dot
	@ make rm-output
	@ make rm-expected
	@ make veryclean
	@ (cd tests/json; make pristine)
	@ for file in $(TARGETS) examples; \
	  do \
	     rm -rf $${file}.pdf $${file}.txt; \
		  rm -rf $${file}.json $${file}*.c; \
		  rm -rf $${file}.pytex $${file}.cdbtex; \
		  rm -rf $${file}.pytex $${file}*.cdbcopy; \
	  done
#-------------------------------------------------------------------------------
# prepare files for github
github:
	@ make pristine
	@ make all
	@ make expected
	@ make veryclean
	@ make rm-output
