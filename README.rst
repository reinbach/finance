Finance
=======

Application to handle finances by;

- Tracking Accounts
- Reading QFX format files
- Calculating budgeted expenses

Objective
---------

Tracking charges/expenses on credit cards and checking accounts. Determine which savings accounts cover the charges/expenses


Install
-------

API
~~~

Initialize the database;

.. code::

  from finance.database import init_db
  init_db()

Add admin user;

.. code::

   from finance.models.user import User, db_session
   u = User('admin', 'secret')
   db_session.add(u)
   db_session.commit()

This is a little long winded at the moment, need to create wrappers to simplify this a lot more.
