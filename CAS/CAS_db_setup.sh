#!/bin/bash
ARGS=("$@")
NUM_ARGS=${#ARGS[@]}
if [ $# -lt 1 ]; then
    echo "Acceptable script usage: sh CAS_db_setup.sh MYSQL_ADMIN_USER"
else 
    ADMIN_USER=${ARGS[0]}
    `mysql -u $ADMIN_USER -p < ubertool_db_creation.sql`
    `mysql -D ubertool -u $ADMIN_USER -p < cas.sql`
fi
