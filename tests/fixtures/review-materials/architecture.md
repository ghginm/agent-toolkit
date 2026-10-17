# Dispatch service — supplied design review

This is synthetic design documentation, not inspected application code. No
runtime measurements or implementation verification accompany this review.

## Purpose and current design

Receive partner jobs, validate them, save them, and notify a delivery partner.
Current documented flow: HTTP intake → validation → SQL job table → inline
partner notification → HTTP response. Validation rejects malformed jobs before
persistence. The partner may be unavailable after a job is saved; callers then
retry and can create duplicate jobs. The SQL job ID is used in support queries.
An admin CLI reads the same table. No retry worker is described in these inputs.

Intake accepts a partner ID and payload. Validation produces a normalized job
or a field-level error. Persistence assigns the job ID. Notification sends the
job ID to the partner. The HTTP request stays open while notification runs.
Existing validation rules are regarded as satisfactory for the current partner;
no redesign of them is proposed in this review.

## Requirements and history

R-01 — Confirmed in the supplied kickoff record: keep job IDs stable for support
and admin CLI consumers. R-02 — Proposal only: notify within five seconds; no
team-approved latency objective exists in these materials. The prior trial
record says an in-memory retry list lost pending jobs on restart. It contains
no load figures or rationale for originally choosing inline notification.

## Proposed direction — not implemented

Consider a durable retry worker. Options: SQL outbox plus worker, managed queue
plus worker, or retain inline notification with documented manual recovery.
An outbox can commit the job and pending delivery together, but adds a worker,
retry policy, and operations. A managed queue may separate scaling concerns,
but introduces another service and a database/queue consistency boundary.
Retaining inline notification is simplest but preserves the failure window.

Backbone questions: delivery guarantee and durable handoff boundary; keep SQL
job IDs or introduce a new external identifier; define an intake deduplication
contract before choosing retry details. Local questions: retry limits, partner
timeouts, and operator visibility. No option is agreed. Team size is small;
traffic, failure frequency, latency targets, and operational budget are unknown.

## External advisory note

A supplied general reliability guide recommends durable handoffs and duplicate-
tolerant delivery. This informs alternatives only. It does not establish that
this service has an outbox, idempotency keys, monitoring, or a working worker.
