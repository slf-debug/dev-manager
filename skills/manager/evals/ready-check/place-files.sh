#!/usr/bin/env bash
set -eu
cp -R "$(dirname "$0")/files/." .
bash ./build-fixture.sh kickoff >/dev/null
bash ./ready-overlay.sh >/dev/null
mkdir -p OUT
