# General attack classes

Select classes by the boundary, not by checklist completion. For each, name the
invariant and trace a controllable input to a concrete unauthorized result. Follow
stored/derived copies and alternate routes; stop at the smallest demonstrated effect.

- **Injection:** compare the input's original context with SQL, HTML, shell,
  template, path, URL or deserialization sinks. Check parameterization/encoding at
  the final sink, including field names, metadata and second-order use.
- **Access control:** authenticate the caller, then bind action and final resource
  to that caller's authority. Compare detail, list, export, batch and legacy paths;
  a tenant field is not enforcement and authentication is not ownership.
- **Resources and files:** examine path normalization, symlinks, archive extraction,
  check/use races, URL redirects and SSRF destinations. Establish lower-trust
  control and the protected destination; unknown network topology is a blocker.
- **Cryptography and secrets:** trace generation, storage, verification, scope,
  rotation and failure fallback. Verify pinned library defaults. Distinguish public
  identifiers from credentials and weak style from actual loss of confidentiality
  or integrity. Never copy real secrets into reports.
- **Business logic:** reconstruct allowed states and accounting invariants. Compare
  negative/zero/overflow values, replay, races, stale/revoked state, partial failure,
  cancellation and rollback only where the interface permits them.
- **Data leakage and feature abuse:** compare authorization across search, export,
  backup, restore, previews, notifications, caches and error responses. State whose
  non-public data is disclosed, not merely that two responses differ.
- **Chained trust:** prove every prerequisite from one component's output to the
  next component's assumed guarantee. Do not infer later authority from an earlier
  parser failure or assume a revoked capability is accepted without tracing it.
- **Shared availability:** bound attacker cost, shared resource, quota/isolation
  failure and effect on others. Ordinary expensive work or self-impact is not a
  shared-service outage. Do not stress-test a live service.

Unexpected code is a lead, not a finding. A missing best practice goes in hardening
unless a reachable boundary violation is established. Use selected domain companions
for additional invariants, never as a replacement for these source traces.
