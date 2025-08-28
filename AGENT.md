# AGENT Instructions

This repository contains multiple services for Trainium Career Navigator.

- Use conventional commit messages.
- For Python services (agents, backend, jobspy_service), run `python -m py_compile` on changed modules.
- When the Kong configuration is modified, validate it with `python -c 'import yaml,sys; yaml.safe_load(open("gateway/kong.yml"))'`.
- The frontend and documentation currently have no automated checks.

