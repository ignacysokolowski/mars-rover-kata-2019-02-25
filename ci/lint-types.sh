#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/../src"

../venv/bin/python -m mypy \
  --junit-xml ../ci/lint/reports/mypy.xml \
  --html-report ../ci/lint/reports/coverage-mypy .
