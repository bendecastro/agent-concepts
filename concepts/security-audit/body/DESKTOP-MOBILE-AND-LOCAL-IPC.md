# Desktop, mobile and local IPC boundaries

Load only when recon finds deep links, exported components, webview bridges,
local daemons/channels, installers or privileged helpers. Distinguish remote content,
another app, another OS user and sandboxed children from the intended same user.

Inventory callable components with OS identity, privilege and protected operation.
Read packaging inputs, entitlements, merged manifests, socket/pipe ACLs and helper
policy. Caller-supplied process names, paths or package IDs are not peer authentication.
Bind OS-authenticated peer identity to every method and final normalized resource.

Trace deep-link and account callbacks to initiating session, app, tenant, action,
expiry and one-time state. Check stale links, duplicate fields, account switching,
notifications and deferred confirmations. For webviews, bind bridge calls to origin
at call time after redirects, subframes and fallback navigation; restrict native
methods and returned data rather than trusting the initial page.

For privileged helpers/installers, follow arguments and mutable files after approval
to the final command/path. Check symlink replacement, descriptor inheritance,
request/handle reuse and privileged repair/update state. Trace local secrets and
cached data across profile switch, logout, backup and restore.

Confirm a meaningful unauthorized operation/disclosure across the named OS/app
boundary, not same-account self-harm or plaintext available only to its intended
owner. Unknown final packaging, signing, OS permissions, device policy or runtime
consent becomes a specific needs-validation blocker. Dummy profiles only, with
owner approval and the no-network scratch-only execution sandbox; never interact
with another user's apps or credentials.
