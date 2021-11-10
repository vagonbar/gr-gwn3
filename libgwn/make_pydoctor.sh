#!/bin/bash
# make_pydoctor.sh: invoca pydoctor para documentación de GWN3
#   must be run from the build directory, thus:
#      ../libgwn/make_pydoctor.sh
#

CURDIR=`pwd`
ISBUILD=`pwd | grep build$`
if [ -n $ISBUILD ]
then
  echo "Directorio actual: " $CURDIR
else
  echo "make_pydoctor: must execute from build directory"
  exit
fi

cd ../..
echo "Directorio de ejecución: " `pwd`
pydoctor --make-html --html-output=gr-gwn3/libgwn/html --project-name="GWN 3" --add-package=gr-gwn3
cd $CURDIR
echo -n "Directorio actual"; pwd

