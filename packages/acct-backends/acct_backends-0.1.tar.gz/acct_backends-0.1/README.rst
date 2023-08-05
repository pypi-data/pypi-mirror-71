=============
ACCT-BACKENDS
=============

============
INSTALLATION
============

`acct-backends` can be installed via pip:
`pip install acct-backends`

============================
INSTALLATION FOR DEVELOPMENT
============================

1. Clone the `acct-backends` repository and install with pip:
`pip install -r requirements.txt`
2. Run `pip install -e <path to provider>` from your project's root directory

You are now fully set up to begin developing acct plugins.

===
USE
===

After installation new acct backends can be specified in your encrypted acct profile::

    acct-backend:
        lastpass:
            username: user@example.com
            password: password
            folder_key: acct-provider-
        keybase:
            username: user
            password: password

