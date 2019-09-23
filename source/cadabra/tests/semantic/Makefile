#-------------------------------------------------------------------------------
SHELL = /bin/bash
#-------------------------------------------------------------------------------
.PHONY: all clean veryclean
#-------------------------------------------------------------------------------
TARGETS = $(patsubst %.tex,%,$(wildcard example-[0-9][0-9]*.tex))
#-------------------------------------------------------------------------------
all:
	@ for file in $(TARGETS); do make .$${file}; done;
	@ # make shared
	@ make summary
	@ make veryclean
#-------------------------------------------------------------------------------
%:
	@ make .$*
.%:	%.tex output/%.json expected/%.json
	@ echo "> cdblatex.sh $* ..."
	@ cdblatex.sh -skx -i $* &> $*.cdblog
	@ pdflatex -halt-on-error -interaction=batchmode $* &> $*.cdblog
	@ touch .redo-summary
	@ touch .$*
#-------------------------------------------------------------------------------
shared:
	@ cadabra2python shared.cdb shared.py
#-------------------------------------------------------------------------------
summary:
	@ make .summary
.summary: .redo-summary
	@ echo "> pdflatex summary ..."
	@ pdflatex -halt-on-error -interaction=batchmode summary &> summary.log
	@ touch .summary
.redo-summary:
	@ touch .redo-summary
#-------------------------------------------------------------------------------
rm-dot:
	@ for file in $(TARGETS) summary; \
	  do \
	     rm -rf .$${file}; \
	  done
	@ rm -rf .[a-z]*.lb
	@ rm -rf .summary .redo-summary
	@ rm -rf .merged.tex .tmp.txt
#-------------------------------------------------------------------------------
rm-output:
	@ rm -rf output/*
#-------------------------------------------------------------------------------
rm-expected:
	@ rm -rf expected/*
#-------------------------------------------------------------------------------
clean:
	@ for file in $(TARGETS) summary; \
	  do \
	     rm -rf $${file}.aux $${file}.log $${file}.out $${file}.synctex.gz; \
	  done
#-------------------------------------------------------------------------------
veryclean:
	@ make clean
	@ for file in $(TARGETS); \
	  do \
	     rm -rf $${file}.cdb $${file}_.cdb; \
		  rm -rf $${file}.cdbidx $${file}.cdbtxt $${file}.cdblog; \
		  rm -rf $${file}.cdbtex $${file}.txt; \
		  rm -rf $${file}.py; \
	  done
#-------------------------------------------------------------------------------
pristine:
	@ make rm-dot
	@ make rm-output
	@ make rm-expected
	@ make veryclean
	@ for file in $(TARGETS) summary; \
	  do \
	     rm -rf $${file}.pdf; \
		  rm -rf $${file}.json $${file}*.c; \
		  rm -rf $${file}.cdbtex $${file}*.cdbcopy; \
	  done
