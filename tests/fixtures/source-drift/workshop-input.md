# Discussion request

Goal: agree on reliable invoice delivery before choosing local retry settings.
Current documented design: CSV → normalization/deduplication → totals → durable outbox.
Legacy README may be outdated. The optional private transport is not supplied.

Choices requiring discussion:
- Keep inline delivery, or introduce a durable pending-delivery boundary?
- Once that is decided, where should retry state live and what evidence should
  determine retry limits? No throughput or latency measurements exist yet.
- Should integer cents remain the internal money contract?

Existing team rule: retain regression tests for behavior changes.
Proposed engineering rule: require a version note for public contract changes.
These engineering practices should not masquerade as pipeline stages.
No meeting has happened and no option has been approved.
