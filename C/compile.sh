#!/bin/bash

if [[ -n "$1" ]]; then
    gcc -O -Wall -W -pedantic -ansi -std=c99 -o test $1
    echo "===== STAERT ====="
    ./test
    echo "===== END ====="
else
    echo "Argument error!\n"
fi