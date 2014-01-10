#! /bin/sh

set -e

echo "processing..."
today=$(date +"%Y-%m-%d")

# make temp directories if do not exist
mkdir -p ../tmp
mkdir -p ../tmp/download
mkdir -p ../tmp/tmp-original
mkdir -p ../tmp/tmp-unzipped

tmpDIR=../tmp/
cd $tmpDIR

# remove old files
if [ -f "download/original.zip" ]; then
	rm download/original.zip
fi
echo "removed original download"
if [ -f "tmp-original/*.zip" ]; then
	rm tmp-original/*.zip
fi
echo "removed /tmp-original files"
if [ -f "tmp-unzipped/*.zip" ]; then
	rm tmp-unzipped/*.zip
fi
echo "removed /tmp-unzipped files"

# will add download command here 
# for now, copy already downloaded file
cp -f ../data_store/dm_spl_release_human_rx_part1.zip download/original.zip
echo "original file downloaded"

# unzips main files to get individual zipped files
ORIGNDATA=tmp-original/
cd $ORIGNDATA

unzip -qj ../download/original.zip
echo "original file unzipped to /tmp-original"

# loop through all individual zipped files to unzip
FILES=*.zip
for f in $FILES
do 
	unzip -qo $f -d ../tmp-unzipped -x *.jpg *.JPG
	# not including image file for now
done
echo "all files unzipped."
echo "processing complete."
# now all original XML files are located in the /tmp-original/[today's date] folder
