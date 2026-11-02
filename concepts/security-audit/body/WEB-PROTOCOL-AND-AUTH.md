# Web protocol and authentication boundaries

Load only when recon finds HTTP parsing/caching, browser credentials or identity
issuance/consumption boundaries. Establish whether the target issues or consumes
each credential; the required bindings differ by role.

- Compare front/back parsing, normalization and cache keys for the exact same input.
  Framing or cache claims require two interpretations and cross-request/user impact.
- Trace trusted proxy/host/origin metadata into routing, reset URLs and identity.
  Do not assume deployed ingress strips hostile headers.
- For ambient-cookie mutations, establish accepted cross-site shape, cookie policy
  and effective CSRF/origin checks. Read-only or non-ambient bearer routes differ.
- Check session rotation and invalidation on login, logout, account switch, recovery
  and privilege changes, including caches and parallel APIs.
- Bind JWT signature, pinned algorithm/key source, issuer, audience, lifetime and
  resource. Bind OAuth/OIDC state, PKCE, redirect, nonce and provider to the initiating
  session; ensure SAML uses the signed element as identity with replay controls.
- For MFA/passkeys/recovery/linking, bind current principal, required assurance,
  origin/RP, challenge, new identity, action, expiry and one-time state. Compare
  fallback and retry routes. API keys need per-resource scope, not just lookup;
  mTLS needs authenticated channel-to-application identity binding.

A missing header, cookie flag or rate limit alone is hardening. Confirm an accepted
invalid credential/transition, unauthorized data/action or demonstrated disclosure.
Unknown proxy, browser, IdP, certificate or deployed policy remains needs_validation
with the exact owner-observable fact. Use dummy offline tokens/requests only if the
run's execution gate is met; never probe deployed identity systems.
