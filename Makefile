#
# Development by Carl J. Nobile
#
# $Author$
# $Date$
# $Revision$
#

PREFIX		= $(shell pwd)
PACKAGE_DIR     = $(shell echo $${PWD\#\#*/})
CHANGE_LOG	= ChangeLog
DOCS		= $(PREFIX)/docs

#----------------------------------------------------------------------
all	: doc tar

#----------------------------------------------------------------------
doc	:
	@(cd $(DOCS); make)

#----------------------------------------------------------------------
log	:
	@rcs2log -h tetrasys.homelinux.org > $(CHANGE_LOG)

#----------------------------------------------------------------------
tar	: clean log
	@(cd ..; tar -czvf $(PACKAGE_DIR).tar.gz --exclude="CVS" \
          $(PACKAGE_DIR))

#----------------------------------------------------------------------
clean	:
	@rm -f *~ \#* .\#* *.pyc
	@(cd ${DOCS}; make clean)

clobber	: clean
	@rm -f $(CHANGE_LOG)
	@(cd ${DOCS}; make clobber)
