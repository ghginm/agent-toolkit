```
module: delivery
status: verified-static
verified_revision: none
verified_at: 2026-10-14
sources:
  - app/delivery.py
  - app/config.py
depends-on: []
```

# Delivery

## Responsibility and contract
Delegates delivery to a configured external transport.

`app/delivery.py::publish` loads `app/config.py::DELIVERY_PLUGIN`. Transport internals were not inspected.
