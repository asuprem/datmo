#!/bin/bash -e

CHANGED_FILES=`git diff --name-only $TRAVIS_COMMIT_RANGE | grep .py$ | grep -v docs/ | grep -v examples/ | grep -v templates/`

exit_success () {
    echo "Passed Formatting Test"
    exit 0
}

if [ -z $CHANGED_FILES ]
then
    echo "No Python Files Changed"
    exit_success
fi

yapf -d $CHANGED_FILES > diff.txt

if [ -s diff.txt ]
then
    cat diff.txt
    echo ""
    echo "Failing Formatting Test"
    echo "Please run yapf over the files changed"
    echo "pip install yapf==0.20.0"
    echo "yapf -i $CHANGED_FILES"
#    exit 1
    exit 0 # shows errors but does not stop travis build
else
    exit_success
fi
#exit 1
exit 0 # shows errors but does not stop travis build