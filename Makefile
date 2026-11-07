.DEFAULT_GOAL := help

# Resolve paths relative to this Makefile, including when invoked with make -f.
REPO_ROOT := $(shell dirname -- "$(MAKEFILE_LIST)")

# Default to this repository's identified tracing implementation; override explicitly.
IMPL ?= .suite/001_portable_tracing
export IMPL

.PHONY: help trace cleanup clean clean-runs clean-tasks

help:
	@echo "make trace        Refresh agent insights with a Perfetto link (optional IMPL=path)"
	@echo "make cleanup      Remove all .suite/ records and transient artifacts"
	@echo "make clean        Remove run evidence and task records (optional IMPL=path)"
	@echo "make clean-runs   Remove runs/ under IMPL"
	@echo "make clean-tasks  Remove tasks/ under IMPL"

trace:
	@cd "$(REPO_ROOT)" && python3 spec-source-suite/helpers/trace_view.py "$$IMPL"

cleanup:
	@cd "$(REPO_ROOT)" && rm -rf -- .suite

clean: clean-runs clean-tasks

clean-runs:
	@cd "$(REPO_ROOT)" && rm -rf -- "$${IMPL:?IMPL must identify an implementation directory}/runs"

clean-tasks:
	@cd "$(REPO_ROOT)" && rm -rf -- "$${IMPL:?IMPL must identify an implementation directory}/tasks"
