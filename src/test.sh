#!/bin/bash

for file in $(find ./tests -type f )
do
    echo "File: $file $(./SLSparser -c $file 2>/dev/null | tail -1)"
done
