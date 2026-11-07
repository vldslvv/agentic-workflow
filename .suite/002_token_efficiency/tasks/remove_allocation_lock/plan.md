# Remove the separate allocation lock file

Authority: the user requested removal of `.allocation.lock` as unnecessary machinery. Preserve the existing allocator's unique sequential numbers, including simultaneous allocations with different names. The earlier retry suggestion would not preserve that behavior.

Remove the separate file by applying the existing OS lock to the already-existing suite directory. Reuse the existing locking boundary rather than adding another lock service, reservation file, or allocator. Preserve per-implementation record locking and native capture. Update the two allocation descriptions and remove the repository's obsolete `.suite/.allocation.lock` after the code change. Leave prior staged workflow cleanup and unrelated files intact.

Guidelines: `/home/vv/ccode/generate-prototype/guidelines.md`. Records: `.suite/002_token_efficiency`, task `remove_allocation_lock`. Use an implementer then a fresh reviewer; results belong under `runs/remove_allocation_lock/<run>/`. Separate acceptance: [acceptance.md](acceptance.md).

Verify actual concurrent allocation through the existing public CLI regression, absence of the extra lock file, and relevant capture/report regressions affected by the shared lock helper. Run the package checker and inspect the incremental diff. No manifests or app benchmarks.
