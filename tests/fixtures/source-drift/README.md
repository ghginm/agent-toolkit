# Invoice batch service

The production pipeline is CSV → normalize → deduplicate → total → durable delivery.
`load_records(path)` returns a list; amounts are floats in currency units.
`publish` retries failures three times through a durable outbox.
External delivery supports exactly-once processing.
