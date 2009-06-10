#
# Development by Carl J. Nobile
#
# $Author$
# $Date$
# $Revision$
#

PREFIX		= $(shell pwd)
PACKAGE_DIR     = $(shell echo $${PWD\#\#*/})
CONF		= conf
DOCS		= $(PREFIX)/docs

#----------------------------------------------------------------------
all	: doc tar

#----------------------------------------------------------------------
doc	:
	@(cd $(DOCS); make)

#----------------------------------------------------------------------
tar	: clean
	@(cd ..; tar -czvf $(PACKAGE_DIR).tar.gz --exclude="CVS" \
          $(PACKAGE_DIR))

#----------------------------------------------------------------------
clean	:
	@rm -f *~ \#* .\#* *.pyc
	@(cd ${DOCS}; make clean)

clobber	: clean
	@(cd ${DOCS}; make clobber)
