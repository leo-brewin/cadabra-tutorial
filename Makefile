SHELL = /bin/bash
#-------------------------------------------------------------------------------
.PHONY:	exercises examples pdf tutorial
#-------------------------------------------------------------------------------
all:
	@ make exercises
	@ make examples
	@ make tutorial
	@ make pdf
	@ make veryclean
#-------------------------------------------------------------------------------
exercises:
	@ echo "> make exercises ..."
	@ (cd source/cadabra/exercises; make)
#-------------------------------------------------------------------------------
examples:
	@ echo "> make examples ..."
	@ (cd source/cadabra; make)
#-------------------------------------------------------------------------------
tutorial:
	@ echo "> make tutorial ..."
	@ (cd source/tex; make)
#-------------------------------------------------------------------------------
pdf:
	@ echo "> make pdf ..."
	@ (cp source/tex/tutorial.pdf pdf/.)
	@ (cp source/cadabra/examples.pdf pdf/.)
	@ (cp source/cadabra/exercises/exercises.pdf pdf/.)
#-------------------------------------------------------------------------------
rm-dot:
	@ (cd source/cadabra/exercises; make rm-dot)
	@ (cd source/cadabra;           make rm-dot)
	@ (cd source/tex;               make rm-dot)
#-------------------------------------------------------------------------------
clean:
	@ (cd source/cadabra/exercises; make clean)
	@ (cd source/cadabra;           make clean)
	@ (cd source/tex;               make clean)
#-------------------------------------------------------------------------------
veryclean:
	@ (cd source/cadabra/exercises; make veryclean)
	@ (cd source/cadabra;           make veryclean)
	@ (cd source/tex;               make veryclean)
#-------------------------------------------------------------------------------
pristine:
	@ rm -rf pdf/*
	@ (cd source/cadabra/exercises; make pristine)
	@ (cd source/cadabra;           make pristine)
	@ (cd source/tex;               make pristine)
#-------------------------------------------------------------------------------
github:
	@ rm -rf pdf/*
	@ (cd source/cadabra/exercises; make github)
	@ (cd source/cadabra;           make github)
	@ (cd source/tex;               make github)
