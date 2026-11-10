.DEFAULT_GOAL := help

# Resolve paths relative to this Makefile, including when invoked with make -f.
REPO_ROOT := $(shell cd "$$(dirname -- "$(MAKEFILE_LIST)")" && pwd)
PYTHON ?= python3
UV ?= uv
PORTABILITY_PYTHONS ?= 3.11 3.15
export PYTHON

# Identify an implementation explicitly for trace and scoped cleanup.
IMPL ?=
TRACE_INTERVAL ?= 5
export IMPL TRACE_INTERVAL
EVAL_AGENT_TIMEOUT ?= 1800
EVAL_COMMAND_TIMEOUT ?= 60
SPEC_BUNDLE ?=
SPECS_MODEL ?= gpt-6-astra
SPECS_REASONING ?= medium
SPECS_TIMEOUT ?= 1800
WORKFLOW_REPAIR ?= 0
WORKFLOW_TIMEOUT ?= 1800
WORKFLOW_MODEL ?= gpt-6-astra
WORKFLOW_REASONING ?= medium

.PHONY: check check-package test check-portability help eval eval-workflow eval-specs trace cleanup clean clean-runs clean-tasks

help:
	@echo "make check        Project-wide typing, lint, format and package checks (UV=uv PYTHON=python3)"
	@echo "make test         Package, installation and eval behavior suites"
	@echo "make check-portability  Package checks and all suites on PORTABILITY_PYTHONS='3.11 3.15'"
	@echo "make eval-specs    Report on current specs against bundle templates; no repairs"
	@echo "                       SPEC_BUNDLE=specs/todolist (default: all bundles)"
	@echo "                       SPECS_MODEL=gpt-6-astra SPECS_REASONING=medium SPECS_TIMEOUT=1800 (defaults)"
	@echo "make eval         Evaluate HEAD in a clean temporary worktree; retain reports under .agentic-workflow/evals/todolist-worktrees/"
	@echo "make eval-workflow  Review workflow documents once; WORKFLOW_REPAIR=1 opts into one repair"
	@echo "                       WORKFLOW_MODEL=gpt-6-astra WORKFLOW_REASONING=medium WORKFLOW_TIMEOUT=1800 (defaults)"
	@echo "                       FIXED means mechanical checks passed without independent re-review; partial edits may remain on failure"
	@echo "make trace        Live agent insights until Ctrl+C (IMPL=path required; optional TRACE_INTERVAL=5; restart to change interval)"
	@echo "make cleanup      Remove numbered execution records; retain project settings"
	@echo "make clean        Remove numbered execution records; retain project settings"
	@echo "make clean-runs   Remove runs/ under IMPL"
	@echo "make clean-tasks  Remove tasks/ under IMPL"

eval:
	@cd "$(REPO_ROOT)" && "$(PYTHON)" -B evals/worktree.py --agent-timeout "$(EVAL_AGENT_TIMEOUT)" --command-timeout "$(EVAL_COMMAND_TIMEOUT)"

eval-workflow:
	@cd "$(REPO_ROOT)" && "$(PYTHON)" -B evals/workflow.py $(if $(filter 1,$(WORKFLOW_REPAIR)),--repair) --timeout "$(WORKFLOW_TIMEOUT)" --model "$(WORKFLOW_MODEL)" --reasoning "$(WORKFLOW_REASONING)"

eval-specs:
	@cd "$(REPO_ROOT)" && "$(PYTHON)" -B evals/specs.py $(if $(SPEC_BUNDLE),--bundle "$(SPEC_BUNDLE)") --timeout "$(SPECS_TIMEOUT)" --model "$(SPECS_MODEL)" --reasoning "$(SPECS_REASONING)"

trace:
	@cd "$(REPO_ROOT)" && "$(PYTHON)" agentic-workflow/helpers/trace_view.py "$${IMPL:?Set IMPL to an implementation directory}" "--interval=$$TRACE_INTERVAL"

cleanup:
	@cd "$(REPO_ROOT)" && rm -rf -- .agentic-workflow/records/[0-9]*_*

clean: cleanup

clean-runs:
	@cd "$(REPO_ROOT)" && rm -rf -- "$${IMPL:?IMPL must identify an implementation directory}/runs"

clean-tasks:
	@cd "$(REPO_ROOT)" && rm -rf -- "$${IMPL:?IMPL must identify an implementation directory}/tasks"

check:
	@cd "$(REPO_ROOT)" && "$(UV)" run --locked ruff check
	@cd "$(REPO_ROOT)" && "$(UV)" run --locked ruff format --check
	@cd "$(REPO_ROOT)" && "$(UV)" run --locked mypy
	@$(MAKE) --no-print-directory -f "$(REPO_ROOT)/Makefile" check-package

check-package:
	@cd "$(REPO_ROOT)" && "$(PYTHON)" -B agentic-workflow/helpers/check_package.py --integration-root .

test:
	@cd "$(REPO_ROOT)" && "$(PYTHON)" -B -m unittest discover -s agentic-workflow/tests -v
	@cd "$(REPO_ROOT)" && "$(PYTHON)" -B -m unittest discover -s tests -v
	@cd "$(REPO_ROOT)" && "$(PYTHON)" -B -m unittest discover -s evals/tests -v

check-portability:
	@set -e; cd "$(REPO_ROOT)"; for version in $(PORTABILITY_PYTHONS); do \
		interpreter="$$( "$(UV)" python find "$$version")"; \
		"$$interpreter" --version; \
		$(MAKE) --no-print-directory -f "$(REPO_ROOT)/Makefile" check-package test PYTHON="$$interpreter"; \
	done
