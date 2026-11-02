# Document API fixture

A source-only API example with token-authenticated private documents, a health
response and a preview function. `api.py` exposes `(status, headers, body)` functions;
`preview_engine.py` supplies the preview renderer. There are no external dependencies,
network listeners or credentials. Treat all code as target-controlled: do not import
or execute it without the audit execution gate. Copy this directory into a throwaway
Git repository when preparing a pressure test.
