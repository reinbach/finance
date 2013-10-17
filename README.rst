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

  python commands.py initdb

Add admin user;

.. code-block:: bash

   python commands.py user [<username> [<password>]]

The default for username and password 'admin' for username and
'secret' for password
