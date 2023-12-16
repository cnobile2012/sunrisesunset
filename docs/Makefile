#
# Makefile
# Development by Carl J. Nobile
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
          --name "Sunrise Sunset Calculator" -o docs/api --show-private \
          --show-imports --graph all --url "${URL}" *.py \
         )
#----------------------------------------------------------------------
tar	:
	@(ln -s ${API_DIR} ${TARBALL_NAME}; \
          tar -chzvf ${TARBALL_NAME}.tar.gz ${TARBALL_NAME})
#----------------------------------------------------------------------
.PHONY	: clean clobber

clean	:
	@rm -f *~ \#* .\#*

clobber	: clean
	@rm -rf ${API_DIR} ${TARBALL_NAME} ${TARBALL_NAME}.tar.gz
