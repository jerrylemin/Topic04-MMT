# Lab04 Codex context

Lab04 is a loopback-only Flask teaching lab for CSRF. The Victim App is fixed at
`http://127.0.0.1:5004`; the Demo Page is fixed at `http://127.0.0.1:9004`.
The vulnerable email flow intentionally omits CSRF validation. Secure mutations,
logout, and reset require session authentication, exact Origin/Referer validation,
and a synchronizer token. Runtime inspectors and evidence must redact secrets.

