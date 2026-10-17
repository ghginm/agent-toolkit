# Dispatch design meeting — synthetic notes

Source: meeting note M-01. No date or participant list was supplied.

- Explicit agreement: preserve existing SQL job IDs for support and the admin
  CLI. This resolves the identifier choice.
- Explicit deferral: choose SQL outbox versus managed queue only after measuring
  failure frequency and clarifying operational budget. No delivery mechanism
  was approved.
- Explicit rejection: do not revive the in-memory retry list; the prior trial
  lost pending jobs on restart. This rejects that option, not durable retries.
- Unresolved: is the proposed five-second notification objective actually a
  requirement? Nobody confirmed it.
- One attendee suggested exponential backoff. No decision was recorded.
