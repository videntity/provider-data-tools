#!/bin/bash
#UPLOAD_DIR="/data/provider-data-tools/pdt/data/test"

#UPLOAD_DIR = $1
#S3_ENDPOINT = $2  #"s3://providers.npi.io/npi/"
echo "Creating provider CDN @ $2 from $1"
echo pwd
for i in $(find . -type d)
do
    if [ $i != "." ] 
      then
        echo  "Directory: $1/$i"
        cd $1/$i
        echo "s3cmd put --acl-public -m application/json  1* $2"
        s3cmd put --acl-public -m application/json  1* $2
        cd $1
    fi
done

