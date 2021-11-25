#! /bin/bash

mkdir -p ../pdf

(cd cadabra/exercises; make; make veryclean)
(cd cadabra; make; make veryclean)
(cd tex; make; make veryclean)
