# User Management

A minimal user management library that supports:

* Email/password sign‑up
* Google OAuth sign‑up (by ID)
* Password validation
* Simple per‑IP rate limiting for sign‑up attempts (max 5 attempts per minute)
* Session cookie creation (HTTP‑only, 30‑day expiry)
* Retrieval of a user from a session identifier

The implementation uses only the Python standard library and is fully covered by the provided tests.
