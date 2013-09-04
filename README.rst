Finance
=======

Application to handle finances by;

- Tracking Accounts
- Reading QFX format files
- Calculating budgeted expenses

Objective
---------

Tracking charges/expenses on credit cards and checking accounts.
Determine which savings accounts cover the charges/expenses


Install
-------

API
~~~

Initialize the database;

.. code-block:: bash

  python install.py initdb

Add admin user;

.. code-block:: bash

   python install.py user [<username> [<password>]]

If no username, password provided then it will default to using 'admin' for
username and 'secret' for password
