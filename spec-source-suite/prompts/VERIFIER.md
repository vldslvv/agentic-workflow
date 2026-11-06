# Frozen check execution

Reviewer/controlled executor: identify requirement mapping, check/fixture/adapter revision, candidate and environment. Execute prescribed checks independently and retain actual command arguments, working directory, start, exit/signal, stdout/stderr, duration and timeout disposition. The [check helper](../docs/HELPERS.md#check-execution) provides durable execution records; it cannot assess coverage or grant acceptance.

Run setup and cleanup as declared, retaining cleanup errors separately from the original failure. Infrastructure timeouts are BLOCKED; a timeout asserting a declared behavioral deadline is FAIL. Missing tools/services or skipped mandatory execution cannot pass. Apply frozen sampling/thresholds. Authorized manual decisions record authority and artifact separately.

Verify baseline and candidate identities before/after. Preserve failures and report suspected verifier defects to the supervisor. Keep expectations unchanged during execution. Return requirement-linked results and raw evidence for this attempt; preserve prior attempts. Avoid duplicate reruns within a role when valid identical evidence exists, while retaining independent review and final assembled-app execution.
