#-------------------------------------------------------------------------------
SHELL = /bin/bash
#-------------------------------------------------------------------------------
.PHONY: all clean veryclean
#-------------------------------------------------------------------------------
TARGETS = $(patsubst %.tex,%,$(wildcard example-[0-9][0-9]*.tex))
#-------------------------------------------------------------------------------
all:
	@ for file in $(TARGETS); do make $${file}; done;
	@ make summary
#-------------------------------------------------------------------------------
%:
	@ echo "> cdblatex.sh $* ..."
	@ cdblatex.sh -skx -i $* &> $*.cdblog
	@ pdflatex -halt-on-error -interaction=batchmode $* &> $*.cdblog
#-------------------------------------------------------------------------------
summary:
	@ echo "> pdflatex summary ..."
	@ pdflatex -halt-on-error -interaction=batchmode summary &> summary.log
#-------------------------------------------------------------------------------
clean:
	@ for file in $(TARGETS) summary; \
	  do \
	     rm -rf $${file}.aux $${file}.log $${file}.out $${file}.synctex.gz; \
	  done
#-------------------------------------------------------------------------------
veryclean:
	@ make clean
	@ for file in $(TARGETS) summary; \
	  do \
		  rm -rf $${file}.cdb $${file}_.cdb; \
		  rm -rf $${file}.cdbidx $${file}.cdbtxt $${file}.cdblog $${file}*.cdbcopy; \
		  rm -rf $${file}.py $${file}.pytxt $${file}.pylog; \
	  done
#-------------------------------------------------------------------------------
pristine:
	@ make veryclean
	@ for file in $(TARGETS) summary; \
	  do \
	     rm -rf $${file}.pdf $${file}.txt; \
		  rm -rf $${file}.json $${file}*.c; \
		  rm -rf $${file}.pytex $${file}.cdbtex; \
		  rm -rf $${file}.pytex $${file}*.cdbcopy; \
	  done
