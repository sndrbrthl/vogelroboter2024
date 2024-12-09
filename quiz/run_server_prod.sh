#!/usr/bin/env bash
if [[ "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi
python -m flask run --no-debug --host=localhost --port=5000