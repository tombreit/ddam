# Python requirements for DDAM

Compile actual requirements files via [pip-tools](https://github.com/jazzband/pip-tools) `pip-compile` command:

```bash
pip-compile requirements/prod.in --output-file requirements.txt
pip-compile requirements/dev.in --output-file requirements-dev.txt
```
