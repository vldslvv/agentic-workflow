.DEFAULT_GOAL := help

# Resolve paths relative to this Makefile, including when invoked with make -f.
REPO_ROOT := $(shell dirname -- "$(MAKEFILE_LIST)")

# Identify an implementation explicitly for trace and scoped cleanup.
IMPL ?=
TRACE_INTERVAL ?= 5
export IMPL TRACE_INTERVAL
EVAL_AGENT_TIMEOUT ?= 1800
EVAL_COMMAND_TIMEOUT ?= 60

.PHONY: help eval trace cleanup clean clean-runs clean-tasks

help:
	@echo "make eval         Evaluate HEAD in a clean temporary worktree; retain reports under .evals/todolist-worktrees/"
	@echo "make trace        Live agent insights until Ctrl+C (IMPL=path required; optional TRACE_INTERVAL=5; restart to change interval)"
	@echo "make cleanup      Remove numbered execution records; retain project settings"
	@echo "make clean        Remove numbered execution records; retain project settings"
	@echo "make clean-runs   Remove runs/ under IMPL"
	@echo "make clean-tasks  Remove tasks/ under IMPL"

eval:
	@cd "$(REPO_ROOT)" && python3 -B evals/worktree.py --agent-timeout "$(EVAL_AGENT_TIMEOUT)" --command-timeout "$(EVAL_COMMAND_TIMEOUT)"

trace:
	@cd "$(REPO_ROOT)" && python3 agentic-workflow/helpers/trace_view.py "$${IMPL:?Set IMPL to an implementation directory}" "--interval=$$TRACE_INTERVAL"

cleanup:
	@cd "$(REPO_ROOT)" && rm -rf -- .agentic-workflow/[0-9]*_*

clean: cleanup

clean-runs:
	@cd "$(REPO_ROOT)" && rm -rf -- "$${IMPL:?IMPL must identify an implementation directory}/runs"

clean-tasks:
	@cd "$(REPO_ROOT)" && rm -rf -- "$${IMPL:?IMPL must identify an implementation directory}/tasks"
