# Supervisor orchestration

Keep Supervisor reads and model turns focused on orchestration decisions.

## File reads

- Read only the files needed to assign the work.
- Read the saved Result and any required independent review after the worker reports completion.
- Open additional files only when the next decision requires them.

## Waiting

- Use a native wait that returns when a worker sends a notification.
- Continue waiting after a timeout unless a decision or deadline requires action.
- Contact workers only when their input is needed for a specific decision or blocker.
- Handle routine progress updates in the runtime.

## Configuration and evaluation

- Set the Codex MultiAgentV2 minimum and default wait to 60 seconds.
- Flag sleeps and repeated short waits in the eval.

```toml
[features.multi_agent_v2]
min_wait_timeout_ms = 60000
default_wait_timeout_ms = 60000
```
