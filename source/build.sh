#! /bin/bash

(cd cadabra/exercises; make github)
(cd cadabra; make github)
(cd tex; make github)

mkdir -p ../pdf

cp -rf tex/tutorial.pdf                     ../pdf/tutorial.pdf
cp -rf cadabra/pdf/examples.pdf             ../pdf/examples.pdf
cp -rf cadabra/exercises/pdf/exercises.pdf  ../pdf/exercises.pdf
