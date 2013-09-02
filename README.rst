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

.. code-block:: python

  from finance.database import DB
  DB().init_db()

Add admin user;

.. code-block:: python

   from finance.models.user import User, DB
   db = DB()
   u = User('admin', 'secret')
   db.session.add(u)
   db.session.commit()

This is a little long winded at the moment, need to create wrappers
to simplify this a lot more.
