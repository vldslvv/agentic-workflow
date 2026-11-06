.DEFAULT_GOAL := help

# Resolve paths relative to this Makefile, including when invoked with make -f.
REPO_ROOT := $(shell dirname -- "$(MAKEFILE_LIST)")

.PHONY: help clean clean-runs clean-tasks

help:
	@echo "make clean        Remove run evidence and task records"
	@echo "make clean-runs   Remove .suite/runs/"
	@echo "make clean-tasks  Remove .agents/tasks/"

clean: clean-runs clean-tasks

clean-runs:
	rm -rf -- "$(REPO_ROOT)/.suite/runs"

clean-tasks:
	rm -rf -- "$(REPO_ROOT)/.agents/tasks"
