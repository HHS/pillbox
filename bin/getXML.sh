#! /bin/sh

set -e

NOW=$(date +"%Y-%m-%d")

ORIGNDATA=../tmp/tmp-original/
cd $ORIGNDATA

FILES=*.zip

for f in $FILES
do 
	unzip -qo $f -d ../tmp-unzipped/$NOW -x *.jpg
done

# now all original XML files are located in the /tmp-original/[today's date] folder
