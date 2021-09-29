#!/bin/bash
# make_pydoctor.sh: invoca pydoctor para documentación de GWN3
#   must be run from the build directory, thus:
#      ../libgwn/make_pydoctor.sh
#

CURDIR=`pwd`
echo "Directorio actual: " $CURDIR
cd ../..
echo "Directorio de ejecución: " `pwd`
pydoctor --make-html --html-output=gr-gwn3/libgwn/html --project-name="GWN 3" --add-package=gr-gwn3
cd $CURDIR
pwd

