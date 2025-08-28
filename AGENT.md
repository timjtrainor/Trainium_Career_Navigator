# AGENT Instructions

This repository contains services for Trainium Career Navigator.

- Use conventional commit messages.
- When Python sources change, run `python -m py_compile agents/app/*.py`.
- When the Kong configuration is modified, validate it with:
  `python -c 'import yaml,sys; yaml.safe_load(open("gateway/kong.yml"))'`.
- The frontend has no automated checks yet.

