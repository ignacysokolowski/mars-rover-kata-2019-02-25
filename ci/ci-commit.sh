#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

fswatch -e ".*" -i "\\.py$" src | xargs -n1 -o sh -c "make ci && git add . && git commit -v && git push"
