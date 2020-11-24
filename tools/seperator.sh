#!/bin/sh
# Copyright 2020 by Mack Gregory and probably some others
#
# The script uses the ImageMagick program to do the conversion. Pass in any
# pdfs as arguments and the images will be placed in the output directory set
# at the beginning of the script
#
# The following settings may need changing in your ImageMagick policy.xml file
# inorder to run properly.
# Comment out the rights none for PDF patterns 
# "<!-- <policy domain="coder" rights="none" pattern="PDF" /> -->"
# Modify the line that assigns resource memory to have a significantly higher
# amount "<policy domain="resource" name="memory" value="2GiB"/>"
OUT_DIR="../images"

# These are occassionally hard coded too...
OUT_TYPE=".jpg"
SEPERATOR="x"
set -x
if ! type convert > /dev/null
then
  echo "Could not find the same program used to convert pdf pages to individual images"
  exit 1
fi

mkdir -p $OUT_DIR

for pdf in $*
do
  filename=`basename $pdf`
  convert -density 300 "$pdf" -quality 90 "../images/$filename$OUT_TYPE"
  for image in `ls ../images/$filename*$OUT_TYPE`
  do
    height=`identify -format "%h" $image`
    width=`identify -format "%w" $image`
    mv $image ${image%.jpg}$SEPERATOR$width$SEPERATOR$height$OUT_TYPE 
  done
done


