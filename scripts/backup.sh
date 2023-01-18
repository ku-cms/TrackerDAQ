#!/usr/bin/bash
# backup.sh

# Script to backup Ph2_ACF working areas and e-link data to R drive.

# Setup:
#
# Initialize KU kerberos:
# kinit <your-ku-id>
# klist
# Mount R drive:
# mnt-bean

# Run backup script:
# /home/kucms/TrackerDAQ/TrackerDAQ/scripts/backup.sh

# When you are done:
# umnt-bean
# kdestroy -A

source_path_1=/home/kucms/TrackerDAQ
source_path_2=/data1/kucms/bump_bond
target_path=/mnt/kucms/BEAN_GRP/e-links/kucms-01

# check if R drive is mounted and directory exists
if [ -d ${target_path} ]
then
    # backup
    echo "------------------------"
    echo "--- Starting backup. ---"
    echo "------------------------"

    echo "--- Backing up '${source_path_1}' to '${target_path}' ---"
    time rsync -avz ${source_path_1} ${target_path}
    
    echo "--- Backing up '${source_path_2}' to '${target_path}' ---"
    time rsync -avz ${source_path_2} ${target_path}
    
    echo "------------------------"
    echo "--- Backup complete! ---"
    echo "------------------------"
else
    echo "ERROR: The directory on the R drive '${target_path}' is not found!"
    echo "- First, initialize KU kerberos with 'kinit <your-ku-id>'."
    echo "- Then mount the R drive with 'mnt-bean'."
fi

# info
echo "When you are done using the R drive, you should unmount the R drive and destroy your kerberos with these commands:"
echo "umnt-bean"
echo "kdestroy -A"

