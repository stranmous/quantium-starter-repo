#!/usr/bin/env bash

source ".venv/Scripts/activate" || exit 1

pytest -q
test_status=$?

if [ "$test_status" -eq 0 ]; then
  exit 0
fi

exit 1