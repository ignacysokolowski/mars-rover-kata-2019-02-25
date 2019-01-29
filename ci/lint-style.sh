#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/../src"

EXITCODE=0
echo "Checking code style ..."
../venv/bin/python -m flake8 . || EXITCODE=$?
echo "Checking imports ..."
../venv/bin/python -m isort -q -c --diff -rc . || EXITCODE=$?
exit $EXITCODE
