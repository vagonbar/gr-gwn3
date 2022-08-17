#!/bin/bash
#
# qa_all : runs all QA tests

LS=`ls -1 qa*.py`
for ARCH in $LS
do
    echo $ARCH
    read RSP
    python3 $ARCH
done

