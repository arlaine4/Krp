NAME := krpsim
WORKDIR ?= .
TESTDIR := $(WORKDIR)/tests
SCRIPTDIR ?= $(WORKDIR)/scripts

.PHONY: install clean

install:
	@python3 -m pip install -r requirements.txt
	@python3 -m pip install -e .

clean:
	@python3 setup.py clean
	@rm -rf src/$(NAME)/__pycache__/	2> /dev/null || true
	@rm -rf tests/__pycache__/			2> /dev/null || true
	@rm -rf src/$(NAME).egg-info/ 		2> /dev/null || true
	@find -iname "*.pyc" -delete		2> /dev/null || true
	@python3 $(SCRIPTDIR)/remove_egg-link.py $(NAME)

re: clean install