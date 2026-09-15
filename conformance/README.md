# Credit lease conformance suite

`SPEC.md` and `vectors/*.json` are copied verbatim from schematic-node
(`conformance/` on `main`), the reference implementation for client-mode credit
leases. Do not edit them here: fix or extend them in schematic-node and copy the
result back, or the SDKs stop pinning the same behavior.

`tests/conformance/test_vectors.py` is this repo's runner. The runner is the
only language-specific piece; every SDK reimplements it and must pass the same
vectors.
