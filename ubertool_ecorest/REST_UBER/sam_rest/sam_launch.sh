#!/bin/bash
#Activate the Python virtual environment
export LD_LIBRARY_PATH=/opt/python2.7.10/lib
source /var/www/ubertool/env2.7.10/bin/activate

if [ $# -gt 0 ]; then
    echo '1st command line arg: ' $1
    echo '2nd command line arg: ' $2
    echo '3rd command line arg: ' $3
    SAM_MULTI_PY=$1
    JID=$2
    NAME_TEMP=$3

    #sleep 15  # Testing
    python $SAM_MULTI_PY $JID $NAME_TEMP
else
    echo "Expected arguments missing"
fi