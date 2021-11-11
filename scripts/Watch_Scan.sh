#!/usr/bin/bash
# Watch_Scan.sh

# Input arguments
logFile=$1

# Check that required arguments have been provided
if [ -z "$logFile" ]
then
    echo " - Please provide a log file as the first argument."
    exit 1
fi

# Check if log file exists
if [ ! -f "$logFile" ]
then
    echo "ERROR: the log file \"$logFile\" does not exist"
    exit 1
fi

# Watch error counter from log file
watch -n 1 "grep \"Final counter\" $logFile"

