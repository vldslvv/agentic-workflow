- Separate state and logic
- Use classes that mix state and logic sparingly, only when required
- Localize side effects
- A top-level flow of each module should have a clear, functional-like flow
- Prefer small, Unix-like modules, each module has public API with small set of responsibilities
- Test public behaviours, not internals
- Prefer using real infrastructure for testing, mock only if testing is expensive or destructive or too complex.
- Build with small modules, composing larger architectural structures out of them

