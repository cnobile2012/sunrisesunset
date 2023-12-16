#
# Development by Carl J. Nobile
#
# $Author$
# $Date$
# $Revision$
#

TODAY           = $(shell date +"%Y-%m-%dT%H:%M:%S.%N%:z")
PPREFIX		= $(shell pwd)
BASE_DIR        = $(shell echo $${PWD\#\#*/})
PR_TAG        = # Define the rc<version>
PACKAGE_DIR     = $(BASE_DIR)-$(VERSION)$(PR_TAG)
APP_NAME        = sunrisesunset
DOCS		= $(PREFIX)/docs
RM_REGEX        = '(^.*.pyc$$)|(^.*.wsgic$$)|(^.*~$$)|(.*\#$$)|(^.*,cover$$)'
RM_CMD          = find $(PREFIX) -regextype posix-egrep -regex $(RM_REGEX) \
                  -exec rm {} \;
PIP_ARGS        = # Pass variables for pip install.
TEST_PATH       = # The path to run tests on.

#----------------------------------------------------------------------
.PHONY	: all
all	: help

.PHONY: help
help	:
	@LC_ALL=C $(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : \
                2>/dev/null | awk -v RS= \
                -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data \
                     base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | grep \
                -E -v -e '^[^[:alnum:]]' -e '^$@$$'

#----------------------------------------------------------------------
.PHONY	: tar
tar	: clean log
	@(cd ..; tar -czvf $(PACKAGE_DIR).tar.gz --exclude=".git" \
          --exclude="__pycache__" $(BASE_DIR))

.PHONY	: sphinx
sphinx	: clean
	@(cd $(DOCS); make)

# To add a pre-release candidate such as 'rc1' to a test package name an
# environment variable needs to be set that setup.py can read.
#
# make build PR_TAG=rc1
# make upload-test PR_TAG=rc1
#
# The tarball could then be named sunrisesunset-2.0.0rc1.tar.gz
#
.PHONY	: build
build	: clean
	python setup.py sdist

.PHONY	: upload
upload	: clobber
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload --repository pypi dist/*

.PHONY	: upload-test
upload-test: clobber
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload --repository testpypi dist/*

.PHONY	: install-dev
install-dev:
	pip install $(PIP_ARGS) -r requirements/development.txt

#----------------------------------------------------------------------
.PHONY	: clean clobber

clean	:
	$(shell $(RM_CMD))

clobber	: clean
	@rm -rf build dist *.egg-info
