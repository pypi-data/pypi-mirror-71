# py-commons
Common code shared by python services

### Dependencies

* Python 3.6.5
* Redis 3.x
* Pyenv
* Twine

### Setup

* Clone Repo
* Create Pyenv environment
* Activate pyenv environment
* Run `pip3 install -r requirements.txt`
* Export the following env variables

Env variable | Value
--- | --- 
APP_SETTINGS | local
PC_MILER_KEY | &lt;PC Miler key&gt;
GOOGLE_API_KEY | &lt;Google API key&gt;

### Add new package

1. `pip install <package_name>`
2. `pip freeze > requirements.txt`

### Testing new version locally
* Bump version in setup.py
* Run deploy_to_local.sh
* The new version is now hosted in local pypi server (Verify by visiting http://localhost:8080/)

### Deploy new version to remote pypi server
* Bump version in setup.py
* Export env variables PYPI_USERNAME and PYPI_PASSWORD with corresponding values
* Run deploy_to_remote.sh
* On https://pypi.org/, login using the above credentials to verify that the new version is deployed by looking at the `Release history`
