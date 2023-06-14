#!/bin/bash
#
# qa_all : runs all QA tests

echo "Runs all QA tests"
echo "  y to run test"
echo "  n to skip test"
echo "  q to exit"

LS=`ls -1 qa*.py`
for ARCH in $LS
do
    echo "About to test" $ARCH". Continue?:"
    read RSP
    if [ $RSP == "y" ]
    then
        python3 $ARCH
    elif [ $RSP == "n" ]
    then 
        continue
    else 
        exit
    fi
done

