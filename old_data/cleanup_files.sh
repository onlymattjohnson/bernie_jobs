#!/bin/bash

for f in *.csv
do
    name=`basename $f`
    echo "processing file : $name"

    cut -d"," -f2- $f > new/$name
done