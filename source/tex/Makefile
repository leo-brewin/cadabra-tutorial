#-------------------------------------------------------------------------------
SHELL = /bin/bash
SED   = /usr/local/bin/sed
#-------------------------------------------------------------------------------
.PHONY: all pdf tests
#-------------------------------------------------------------------------------
TARGETS = $(patsubst %.tex,%,$(wildcard tutorial.tex))
#-------------------------------------------------------------------------------
all:
	@ for file in $(TARGETS); do make .$${file}; done;
#-------------------------------------------------------------------------------
%:
	@ make .$*
.%:	%.tex
	@ echo "pdflatex.sh $* ..."
	@ touch $*.aux
	@ pdflatex -halt-on-error -interaction=batchmode $* &> $*.cdblog
	@ bibtex $* &> $*.cdblog
	@ pdflatex -halt-on-error -interaction=batchmode $* &> $*.cdblog
	@ pdflatex -halt-on-error -interaction=batchmode $* &> $*.cdblog
	@ touch .$*
#-------------------------------------------------------------------------------
rm-dot:
	@ for file in $(TARGETS); \
	  do \
	     rm -rf .$${file}; \
	  done
	@ rm -rf .[a-z]*.lb
#-------------------------------------------------------------------------------
clean:
	@ for file in $(TARGETS) examples; \
	  do \
	     rm -rf $${file}.log $${file}.out $${file}.synctex.gz; \
	     rm -rf $${file}.errors $${file}.exnum $${file}.lstnum $${file}.blg; \
	  done
#-------------------------------------------------------------------------------
veryclean:
	@ make clean
	@ for file in $(TARGETS) examples; \
	  do \
	     rm -rf $${file}.aux; \
		  rm -rf $${file}.cdb $${file}_.cdb; \
		  rm -rf $${file}.cdbidx $${file}.cdbtxt $${file}.cdblog; \
		  rm -rf $${file}.py $${file}.pytxt $${file}.pylog; \
	  done
#-------------------------------------------------------------------------------
pristine:
	@ make rm-dot
	@ make veryclean
	@ for file in $(TARGETS) examples; \
	  do \
	     rm -rf $${file}.pdf; \
	  done
#-------------------------------------------------------------------------------
# prepare files for github
github:
	@ make pristine
	@ make all
	@ make veryclean
