PROJECT_TITLE="Replace Me With Your Project Title"
PROJECT_NAME="replace_me_with_your_project_name"
###############################################################################
MAKEFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
PROJECT_PATH:=$(shell dirname $(MAKEFILE_PATH))
MAKEDIR_PATH:=$(PROJECT_PATH)/Makefile.d
VENV_PATH:=$(MAKEDIR_PATH)/.venv

# with-dispatch: hands off to Makefile.d/make.py
# if Makefile.d/requirements.txt exists, creates a venv
define with-dispatch
if [ -f $(MAKEDIR_PATH)/make.py ]; then \
	if [ -f Makefile.d/requirements.txt ]; then \
		if [ ! -f $(VENV_PATH)/bin/activate ]; then \
			echo -e $(call green,"Creating Makefile venv..."); \
			python -m venv $(VENV_PATH); \
			source $(VENV_PATH)/bin/activate; \
			$(VENV_PATH)/bin/pip install -r Makefile.d/requirements.txt; \
		fi; \
		source $(VENV_PATH)/bin/activate; \
	fi; \
	python $(MAKEDIR_PATH)/make.py $(PROJECT_NAME) $(1); \
else \
	echo -e $(call redb,"ERROR: Expects script at Makefile.d/make.py"); \
fi
endef

blueb= "\033[0;95m"$1"\033[0m"
redb="\033[1;31m"$1"\033[0m"
greenb="\033[1;32m"$1"\033[0m"
green="\033[0;32m"$1"\033[0m"

help: print-banner
	@echo -e $(call greenb,"Please use 'make <TARGET>' where <TARGET> is one of:")
	@echo -e $(call green," help")"                   Show this dialogue. (Use "$(call green,"help-all")" for development targets.)"
	@echo -e $(call green," migrate")"                Run 'python manage.py migrate'"
	@echo -e $(call green," migrations")"             Run 'python manage.py makemigrations'"
	@echo -e $(call green," runserver")"              Run the development server."
	@echo -e $(call green," shell")"                  Drop into a bash shell on a container."
	@echo -e $(call green," test")"                   Run functional tests."
	@echo -e $(call green," unittest")"               Run unit tests."


help-all: help
	@echo
	@echo -e $(call greenb,"Further <TARGET> options:")
	@echo -e $(call green," print-banner")"           Used by each target to print the banner."
	@echo -e $(call green," clean")"                  Clean-up artifacts."
	@echo -e $(call green," restore")"                Restore file ownership to match parent dir."
	@echo -e $(call green," startproject")"           WARNING: Edit Makefile to set PROJECT_NAME"

	@echo -e                 "                        before running startproject!"

print-banner:
	@echo -e $(call blueb,"--- ") $(call redb,$(PROJECT_TITLE)) $(call blueb," ---")

clean: print-banner
	@if [ -d $(VENV_PATH) ]; then \
		$(call with-dispatch,clean); \
		echo -e $(call green,"Removing Makefile venv..."); \
		rm -rf $(VENV_PATH); \
	fi

migrate: print-banner
	@$(call with-dispatch,migrate)

migrations: print-banner
	@$(call with-dispatch,migrations)

restore: print-banner
	@$(call with-dispatch,restore)

runserver: print-banner
	@$(call with-dispatch,runserver)

shell: print-banner
	@$(call with-dispatch,shell)

startproject: print-banner
	@$(call with-dispatch,startproject)

test: print-banner
	@$(call with-dispatch,test)

unittest: print-banner
	@$(call with-dispatch,unittest)

