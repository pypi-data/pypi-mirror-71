# sheetgear-noodle

## Installing the development tools

```shell
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
sudo apt install -y build-essential libssl-dev libffi-dev
sudo apt install -y libgdbm-dev libsqlite3-dev zlib1g-dev
sudo apt install -y python3-dev python3-pip python3-venv python3-setuptools
```

## Installing the package from TestPyPI

```shell
python3 -m venv .env
source .env/bin/activate

python3 -m pip install --upgrade setuptools wheel
python3 -m pip install --upgrade ansible

python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
python3 -m pip install --pre -i https://test.pypi.org/simple sheetgear-bridge
python3 -m pip install --pre -i https://test.pypi.org/simple sheetgear-noodle
```

## Installing the package from local

```shell
python3 -m pip install PATH_TO_YOUR.whl
```

## Create the client_secrets and credentials files

Quickstart:

* Open the url: https://developers.google.com/sheets/api/quickstart/python
* Click to [Enable the Google Sheets API]

Another way:

* Open the Google Cloud Dashboard: https://console.cloud.google.com/
* Create a new project
* Open the APIs credentials: https://console.cloud.google.com/apis/credentials
* Create an OAuth 2.0 Client IDs
* Setup an OAuth consent screen
* Download the client_secrets.json file
