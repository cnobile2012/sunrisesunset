#
# Makefile
# Development by Carl J. Nobile
#
# $Author$
# $Date$
# $Revision$
#

FQDN		= $(shell hostname --fqdn)
DOC_DIR		= $(shell pwd)
API_DIR		= api
URL		= http://${FQDN}${DOC_DIR}/${API_DIR}/index.html
TARBALL_NAME	= SunriseSunset

all	: api-docs

#----------------------------------------------------------------------
api-docs:
	@(cd ..; epydoc -v --docformat epytext \
          --name "Python WSGI RESTful Framework" -o docs/api --show-private \
          --show-imports --graph all --url "${URL}" *.py \
         )
#----------------------------------------------------------------------
tar	:
	@(ln -s ${API_DIR} ${TARBALL_NAME}; \
          tar -chzvf ${TARBALL_NAME}.tar.gz ${TARBALL_NAME})
#----------------------------------------------------------------------

clean	:
	@rm -f *~ \#* .\#*

clobber	: clean
	@rm -rf ${API_DIR} ${TARBALL_NAME} ${TARBALL_NAME}.tar.gz 
