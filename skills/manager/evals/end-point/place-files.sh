#!/usr/bin/env bash
set -eu
cp -R "$(dirname "$0")/files/." .
bash ./build-fixture.sh endpoint >/dev/null
mkdir -p OUT
