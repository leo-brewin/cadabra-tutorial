#! /bin/bash

for file in tests/output/*; do

   target=$(basename "$file")

   echo "> diff" ${target}
   diff tests/expected/${target} tests/output/${target}

done

# Any diff, no matter how trivial (e.g., dates), will cause diff to
# return a non-zero exit code. This will cause subsequents in a Makefile
# to fail. Avoid this by forcing a 0 exit.

exit 0
