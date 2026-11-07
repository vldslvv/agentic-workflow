.DEFAULT_GOAL := help

# Resolve paths relative to this Makefile, including when invoked with make -f.
REPO_ROOT := $(shell dirname -- "$(MAKEFILE_LIST)")

# Default to this repository's identified tracing implementation; override explicitly.
IMPL ?= .suite/001_portable_tracing
TRACE_INTERVAL ?= 5
export IMPL TRACE_INTERVAL
EVAL_AGENT_TIMEOUT ?= 1800
EVAL_COMMAND_TIMEOUT ?= 60

.PHONY: help eval trace cleanup clean clean-runs clean-tasks

help:
	@echo "make eval         Evaluate HEAD in a clean temporary worktree; retain reports under .evals/todolist-worktrees/"
	@echo "make trace        Live agent insights until Ctrl+C (optional IMPL=path TRACE_INTERVAL=5; restart to change interval)"
	@echo "make cleanup      Remove all .suite/ records and transient artifacts"
	@echo "make clean        Remove run evidence and task records (optional IMPL=path)"
	@echo "make clean-runs   Remove runs/ under IMPL"
	@echo "make clean-tasks  Remove tasks/ under IMPL"

eval:
	@cd "$(REPO_ROOT)" && python3 -B evals/worktree.py --agent-timeout "$(EVAL_AGENT_TIMEOUT)" --command-timeout "$(EVAL_COMMAND_TIMEOUT)"

trace:
	@cd "$(REPO_ROOT)" && python3 spec-source-suite/helpers/trace_view.py "$$IMPL" "--interval=$$TRACE_INTERVAL"

cleanup:
	@cd "$(REPO_ROOT)" && rm -rf -- .suite

clean: clean-runs clean-tasks

clean-runs:
	@cd "$(REPO_ROOT)" && rm -rf -- "$${IMPL:?IMPL must identify an implementation directory}/runs"

clean-tasks:
	@cd "$(REPO_ROOT)" && rm -rf -- "$${IMPL:?IMPL must identify an implementation directory}/tasks"
