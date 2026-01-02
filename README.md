# Convex API

![](https://github.com/Convex-Dev/convex-api-py/workflows/testing/badge.svg)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)

[Documentation](https://convex-dev.github.io/convex-api-py)

### Development Setup

To set up the project for development, follow these steps:

**Prerequisites:**
- Python 3.10 or higher
- pip (Python package installer)

**Setup Steps:**

1. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```
   
   This creates a virtual environment in a `.venv` directory. 

2. **Activate the virtual environment:**
   
   - **On Windows (PowerShell or Command Prompt):**
     ```bash
     .venv\Scripts\activate
     ```
   
   - **On Windows (Git Bash):**
     ```bash
     source .venv/Scripts/activate
     ```
   
   - **On Linux/Mac:**
     ```bash
     source .venv/bin/activate
     ```
   
   When activated, you should see `(venv)` at the beginning of your command prompt.

3. **Upgrade pip (recommended):**
   ```bash
   python -m pip install --upgrade pip
   ```

4. **Install the package in development mode with all dependencies:**
   
   Option 1 - Using setup.py extras (recommended):
   ```bash
   pip install -e ".[dev,test,docs]"
   ```
   
   Option 2 - Using requirements files:
   ```bash
   pip install -r requirements-dev.txt
   pip install -e .
   ```

5. **Verify the installation:**
   ```bash
   pytest tests
   ```

**Deactivating the virtual environment:**
When you're done working, you can deactivate the virtual environment by running:
```bash
deactivate
```

**Note:** Always activate your virtual environment before working on the project. The virtual environment ensures that dependencies are isolated from your system Python installation.

### Quick Start

First you need to download the Convex-API-py package from the python package index PyPi.

    pip install convex-api

You can now access the convex network, and get a balance from an existing account on the network by doing the following:

    >>> from convex_api import API
    >>> convex = API('https://peer.convex.live')
    >>> convex.get_balance(9)
    99396961137042

You can create a new emtpy account, with now balance:

    >>> key_pair = KeyPair.create()
    >>> account = convex.create_account(key_pair)
    >>> account.address
    809

You can request some funds to the new account and then get the account information:

    >>> convex_api.request_funds(1000000, account)
    1000000
    >>> convex.get_account_info(account)
    {'environment': {}, 'address': 809, 'is_library': False, 'is_actor': False, 'memory_size': 42, 'balance': 1000000, 'allowance': 0, 'sequence': 0, 'type': 'user'}


You can export the accounts private key encoded as PKCS8 encrypt the key with a password:

    >>> account.key_pair.export_to_text('secret')
    '-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIGbMFcGCSqGSIb3DQEFDTBKMCkGCSqGSIb3DQEFDDAcBAiMY42UY4PXHAICCAAw\nDAYIKoZIhvcNAgkFADAdBglghkgBZQMEASoEEJpwDMicGbGj2iSJesktIVYEQBsp\nKMTAHzvUyw8jZRr8WSrmxH7938sjma8XWI6lgd9jwTZzcGamog7p3zatw0Wp+jFK\nKruWAZmIqhBZ/2ezDv8=\n-----END ENCRYPTED PRIVATE KEY-----\n'

    >>> account.address
    809

To re-use your account again you need to import the encrypted private key and set the correct account address

    >>> from api import Account, KeyPair
    >>> key_pair = KeyPair.import_from_file('my_key.dat', 'secret')
    >>> account = Account.create(key_pair, 809)

To create a new address with the same account keys in your new or imported account object, you can do:

    >>> new_account = convex.create_account(key_pair)
    >>> account.address
    809
    >>> new_account.address
    934

To use account names, where an account name is resolved to a fixed address. You can create or load
an account based on it's name by doing the following:

    >>> account = convex.setup_account('my-account-name', key_pair)
    >>> account.address
    934

    >>> convex.resolve_account_name('my-account-name')
    934

    >>> same_account = convex.setup_account('my-account-name', key_pair)
    >>> same_account.address
    934

To submit a transaction, use ConvexAPI.send(). This will cost a small about of juice, and reduce your balance

    >>> convex.request_funds(1000000, account)
    1000000
    >>> convex.send('(map inc [1 2 3 4])', account)
    {'value': [2, 3, 4, 5]}
    >>> convex.get_balance(account)
    996360

To send a query a transaction, this is free and can be performed by any valid account address.
So for example to query a balance of an account:

    >>> convex.query(f'(balance {account.address})', account)
    {'value': 996360}

    # this is the same as above
    >>> convex.query(f'(balance {account.address})', account.address)
    {'value': 996360}

    # get the balance using one of the standard account addresses (#1)
    >>> convex.query(f'(balance {account.address})', 1)
    {'value': 996360}

