#-------------------------------------------------------------------------------
SHELL = /bin/bash
#-------------------------------------------------------------------------------
.PHONY: all
#-------------------------------------------------------------------------------
TARGETS = $(patsubst %.tex,%,$(wildcard tutorial.tex))
#-------------------------------------------------------------------------------
all:
	@ version.sh
	@ for file in $(TARGETS); \
	  do \
	     if ! [[ -e $${file}.aux ]]; then \
		     touch $${file}.aux $${file}.tex; \
		  fi; \
	     make .$${file}; \
	  done
#-------------------------------------------------------------------------------
%:
	@ make .$*
.%:	%.tex
	@ echo "pdflatex $* ..."
	@ touch $*.aux
	@ rm -rf $*.bbl $*.bcf
	@ pdflatex -halt-on-error -interaction=batchmode $* &> $*.tmplog
	@ # pick just one, bibtex or biber, must alter source.tex to suit
	@ # echo "bibtex $* ..."
	@ # bibtex $* &> $*.cdblog
	@ echo "biber $* ..."
	@ biber --decodecharsset=null $* &> $*.cdblog
	@ echo "pdflatex $* ..."
	@ pdflatex -halt-on-error -interaction=batchmode $* &> $*.tmplog
	@ echo "pdflatex $* ..."
	@ pdflatex -halt-on-error -interaction=batchmode $* &> $*.tmplog
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
	@ for file in $(TARGETS); \
	  do \
	     rm -rf $${file}.log $${file}.out $${file}.tmplog $${file}.synctex.gz; \
		  rm -rf $${file}.bcf $${file}.blg $${file}.run.xml; \
	     rm -rf $${file}.errors $${file}.exnum $${file}.itnum $${file}.lstnum $${file}.blg; \
	  done
#-------------------------------------------------------------------------------
veryclean:
	@ make clean
	@ for file in $(TARGETS); \
	  do \
	     rm -rf $${file}.aux $${file}.bbl; \
		  rm -rf $${file}.cdb $${file}_.cdb; \
		  rm -rf $${file}.cdbidx $${file}.cdbtxt $${file}.cdblog; \
		  rm -rf $${file}.py $${file}.pytxt $${file}.pylog; \
	  done
#-------------------------------------------------------------------------------
pristine:
	@ make rm-dot
	@ make veryclean
	@ for file in $(TARGETS); \
	  do \
	     rm -rf $${file}.pdf; \
	  done
#-------------------------------------------------------------------------------
# prepare files for github
github:
	@ make pristine
	@ make all
	@ make veryclean
