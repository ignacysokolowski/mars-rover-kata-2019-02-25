#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/../src"

../venv/bin/python -m pytest \
  -v \
  --cov mars_rover \
  --cov-report term-missing \
  --cov-report html:../ci/test/reports/coverage \
  --junit-xml=../ci/test/reports/results.xml \
  tests
