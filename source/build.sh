#! /bin/bash

mkdir -p ../pdf

(cd cadabra/exercises; make github)
(cd cadabra; make github)
(cd tex; make github)
