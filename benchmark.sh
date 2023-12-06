#!/bin/bash

LOG_FILE='time_stats.txt'

echo -e "Individual runtimes\n" > $LOG_FILE
for i in *.py
do
	echo -e '\n--------------\n'$i >> $LOG_FILE
	{ time python $i; } >> $LOG_FILE 2>&1
done
echo -e "\nTotal runtime\n" >> $LOG_FILE
{ time $(for i in *.py; do python $i > /dev/null; done); } >> $LOG_FILE 2>&1
