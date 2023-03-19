# Python requirements for DDAM

Compile actual requirements files via [pip-tools](https://github.com/jazzband/pip-tools) `pip-compile` command:

```bash
pip-compile prod.in --output-file prod.txt
pip-compile dev.in --output-file dev.txt
```
