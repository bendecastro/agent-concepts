# Supply chain and release boundaries

Load only when recon finds dependencies, untrusted build contributions, CI,
publication, signing, promotion, plugin installation or software updates.

Walk backward from the installed/released digest through promotion, signature,
test, artifact producer, worker, cache and resolved inputs. Verify the same immutable
identity survives every handoff. A mutable dependency is not itself a vulnerability:
name its lower-trust writer and the trusted build or release that consumes it.

Compare untrusted and protected CI events: trigger, checkout ref, executed code,
token permissions, secrets, runner and environment gates. Trace attacker-controlled
workflow expressions into shells. Check cache/artifact/workspace producer trust,
namespace and digest binding before privileged restore or promotion.

Review namespace/registry resolution, lockfiles, downloaded generators, remote
includes and build context for real credential/private-data inclusion. Checksums
from the same hostile origin are not independent authenticity. Verify signing
policy binds repository, workflow, branch/environment, product and artifact digest,
not merely that a signature verifies. Updaters must bind platform, channel, version,
expiry, rollback policy and destination, including failure/repair paths.

Confirm a complete source-visible path to unauthorized publication, code inclusion,
secret disclosure or privileged execution. Hosted branch protections, registry
rules, runner trust or signing-service policy absent from source are blockers, not
assumed absent. Use dummy artifacts only under the execution gate; never publish,
fetch dependencies or mutate a real release. Intended same-user plugin installation
is not by itself a privilege boundary.
