# Assignment — future automated runner

Active only when the user requests runner implementation. The ordinary file-based workflow needs no runner. Read the [shared rules](docs/SUITE_CONTRACT.md), role routines and separate [acceptance list](docs/BUILD_THE_SUITE.md).

1. Inspect repository conventions and available worker tools. Build a small bundle reader/validator, serial dependency scheduler, worker/review adapters, project check adapter and durable result store.
2. Support Define, Implement, Generate, status/resume, incremental work and reconstruction. Reuse the existing bundle and task/run locations. Prepare each task only when its prerequisites pass; retain its implementer through repairs and request fresh review each time.
3. Capture execution session/turn references and use the retained usage helper. Keep unavailable counters explicit and separate from acceptance.
4. Exercise acceptance with abstract fixtures, stub/manual adapters and explicit failures. A manual fallback records its origin; it cannot claim fresh review or execution that did not occur.
5. Report implemented capabilities, actual checks and blockers separately from live generation experiments.

Do not invent an app, select its stack, or add a hosted control plane. Verify installed help before relying on external worker flags. Future automation must follow the simplified workflow without adding mandatory manifests, frozen checks or approval receipts.
