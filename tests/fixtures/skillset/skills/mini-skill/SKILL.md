---
name: mini-skill
description: "Fixture skill used by toolkit tests to prove new independent skills are discovered without installer changes. Use when running agent-toolkit unit tests."
license: MIT
metadata:
  author: agent-toolkit-tests
  version: "0.0.1"
---

# Mini Skill

Fixture-only skill: a valid, self-contained unit with no resources. Tests use it to verify discovery, validation, and installation generalize beyond the toolkit's shipped skills.

## Procedure

Do nothing observable; report "mini-skill executed".
