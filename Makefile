WORKFLOWS_DIR := ~/Library/Application\ Support/Alfred/Alfred.alfredpreferences/workflows
BUNDLE_ID := dk.sniarn.alfred-pricerunner-workflow
WORKFLOW_NAME := PriceRunner

all: dist

dist: clean-dist clean-pyc
	mkdir -p $(CURDIR)/dist
	cd $(CURDIR)/src; zip -r ../dist/$(WORKFLOW_NAME).alfred3workflow *

clean-dist:
	rm -rf $(CURDIR)/dist

clean-pyc:
	find $(CURDIR)/src -name '*.pyc' -delete

link:
	ln -sFhv $(CURDIR)/src $(WORKFLOWS_DIR)/$(BUNDLE_ID)

unlink:
	rm $(WORKFLOWS_DIR)/$(BUNDLE_ID)

update-lib:
	/usr/bin/python -m pip install --target $(CURDIR)/src --no-compile --upgrade Alfred-Workflow

.PHONY: dist clean-dist clean-pyc link unlink update-lib
