# Setup

Create a virtual env and activate it, e.g.:

`virtualenv .venv`

Visual Studio Code will detect this and promt to activate it.

`python -m pip install --upgrade pip`
`pip install -r requirements.txt`

# Sample VS Code launch.json file

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Import Sets (MTGJSON)",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/mtgjson-import-set.py",
            "args": [
            ],
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Convert Dragon Shield",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/dragonshield-convert.py",
            "args": [
            ],
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```
