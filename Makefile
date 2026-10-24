.PHONY: requirements

help:
	@echo "requirements - Updates requirements.txt and requirements-dev.txt"

requirements:
	python3 -m pip install --upgrade pip-tools pip wheel setuptools
	python3 -m piptools compile --generate-hashes --allow-unsafe --upgrade --strip-extras --output-file=requirements.txt      requirements/prod.in
	python3 -m piptools compile --generate-hashes --allow-unsafe --upgrade --strip-extras --output-file=requirements-dev.txt  requirements/dev.in
