# modo2auth-py

> A Python package to generate authentication details to communicate with Modo servers

# Prerequesites

**Credentials** that are created and shared by Modo. These will be different for each environment (`int`, `prod`, `local` etc...).

- `api_identifier` - API key from Modo
- `api_secret` - API secret from Modo

These values will be used when intantiating the library.

`python` - [See docs](https://www.python.org/downloads/)

# Install

## Pipenv (recommended)
Requires [pipenv](https://pipenv.pypa.io/en/latest/)
```python
# In root of your project
pipenv install modo2auth
```

## Copy/Paste
1. Copy `modo2auth/modo2auth.py` to your project.
2. Install required dependencies:
    ```bash
    # for dependencies
    sudo easy_install pip
    # for requests
    sudo pip install requests
    ```


# Example Usage
Here's an example using `TBD` to make requests. You can use your preferred method or library.

Note: if installed with `pipenv`, run shell commands via `pipenv shell`

## `GET` Example
```py
# installs
#   $ sudo easy_install pip
#   $ sudo pip install requests

# 1. IMPORT
import requests
import modo2auth

# 2. INSTANTIATE
# get from Modo
creds = {
    "api_identifier": "...",
    "api_secret":  "..."
}
headers = {
    "Content-Type": "application/json"
}
api_host = "http://localhost:82"  # TODO: replace with stable testing env endpoint
api_uri = "/v2/vault/public_key"

# 3. SEND REQUEST
response = requests.get(
    api_host+api_uri,
    headers=headers,
    auth=modo2auth.Sign(creds['api_identifier'], creds['api_secret'], api_uri))

print(response.text)

```

## `POST` Example
```py
# installs
#   $ sudo easy_install pip
#   $ sudo pip install requests

# 1. IMPORT
import requests
import modo2auth

# 2. INSTANTIATE
# get from Modo
creds = {
    "api_identifier": "...",
    "api_secret":  "..."
}
headers = {
    "Content-Type": "application/json"
}
api_host = "http://localhost:82"  # TODO: replace with stable testing env endpoint
api_uri = "/v2/reports"
data = '{"start_date": "2020-05-22T00:00:00Z","end_date": "2020-05-26T00:00:00Z"}'

# 3. SEND REQUEST
response = requests.post(
    api_host+api_uri,
    headers=headers,
    data=data,
    auth=modo2auth.Sign(creds['api_identifier'], creds['api_secret'], api_uri))

print(response.text)

```



# API

## `Sign(api_identifier, api_secret, api_uri)`

Returns an instance of the `Sign` class. Intended for use with the [`requests`](https://requests.readthedocs.io/en/master/user/authentication/) package.

- `api_identifier` (string) - API key from Modo
- `api_secret` (string) - API secret from Modo
- `api_uri` (string) - Api Uri intending to call to (ex: `"/v2/vault/public_key"`)