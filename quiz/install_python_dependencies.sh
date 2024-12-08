

python -m venv .venv
if [[ "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi
pip3 install --upgrade pip
pip3 install --upgrade wheel
pip3 install -r requirements.txt
deactivate
