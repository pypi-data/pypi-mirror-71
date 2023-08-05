# AA Discord Ping Formatter

App for formatting pings for Discord in Alliance Auth

## Contents

- [Installation](#installation)
- [Updating](#updating)
- [Screenshots](#screenshots)
- [Change Log](CHANGELOG.md)

## Installation

**Important**: This app is a plugin for Alliance Auth. If you don't have Alliance Auth running already, please install it first before proceeding. (see the official [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/allianceauth.html) for details)

### Step 1 - Install app

Make sure you are in the virtual environment (venv) of your Alliance Auth installation. Then install the latest version:

```bash
pip install aa-discord-ping-formatter
```

### Step 2 - Update your AA settings

Configure your AA settings (`local.py`) as follows:

- Add `'discordpingformatter',` to `INSTALLED_APPS`


### Step 3 - Finalize the installation

Run migrations & copy static files

```bash
python manage.py collectstatic
python manage.py migrate
```

Restart your supervisor services for AA

### Step 4 - Setup permissions

Now you can setup permissions in Alliance Auth for your users. Add ``discordpingformatter | aa discord ping formatter | Can access this app`` to the states and/or groups you would like to have access.

## Updating

To update your existing installation of AA Discord Ping Formatter first enable your virtual environment.

Then run the following commands from your AA project directory (the one that contains `manage.py`).

```bash
pip install -U aa-discord-ping-formatter
```

```bash
python manage.py collectstatic
```

```bash
python manage.py migrate
```

Finally restart your AA supervisor services.

## Screenshots

### View in Alliance Auth

![AA View](https://raw.githubusercontent.com/ppfeufer/aa-discord-ping-formatter/development/discordpingformatter/docs/aa-view.jpg)

### Discord Ping

![Discord Ping](https://raw.githubusercontent.com/ppfeufer/aa-discord-ping-formatter/development/discordpingformatter/docs/discord-ping.jpg)
