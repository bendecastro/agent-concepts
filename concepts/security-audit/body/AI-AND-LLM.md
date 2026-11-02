# AI, LLM and agent boundaries

Load only when recon finds untrusted content flowing through a model or memory
into authority, another principal's context or a sensitive sink.

Map identities, capabilities, writable context/memory and output destinations.
Trace retrieval ACLs and cache/session keys; find every writer of persistent memory
and its later consumer. Check prompt role/provenance serialization, but do not call
persuasive text alone a vulnerability: prompts are not deterministic boundaries.

Work backward from tools through handlers, dispatch, schema, confirmation and model
context. Tool schemas constrain shape, not authority. Bind requester, normalized
arguments, final resource and exact approved action at execution, including retries,
queues and resumed turns. Separate confused-deputy authority from action-binding:
a victim may have permission but never have requested the attacker-induced action.

For MCP/delegation, check authenticated peer, tool namespace, outstanding request
correlation, scoped credentials and results on return. Metadata cannot grant policy.
Trace model output into renderers, URLs and commands using sink-specific controls.

Confirm only a code-level control failure with a concrete unauthorized/unrequested
action, cross-principal disclosure or durable authority change. Same-user intentional
use is not privilege gain. Unknown model/provider behavior or renderer/identity
configuration is a precise needs-validation blocker; do not execute model calls or
contact providers to settle it.
