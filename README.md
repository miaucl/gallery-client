# gallery-client

A gallery client collection for simple frontend devices

Have a look at `./clients` to see the available builds.

## Dev

Setup the dev environment using VSCode, it is highly recommended. It might not be possible on your device as the build is targeted to the actual hardware.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r clients/***/requirements.txt
```

Install [pre-commit](https://pre-commit.com)

```bash
pre-commit install

# Run the commit hooks manually
pre-commit run --all-files
```

Following VSCode integrations may be helpful:

- [ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [mypy](https://marketplace.visualstudio.com/items?itemName=matangover.mypy)
- [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)
