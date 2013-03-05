This package will allow you to query for CAS Number related data.
CASGql.py is a script that includes functionality to allow you to query local and GAE CAS-based databases, using the GQL language.
To set up a local CAS database(the default set up), run "./CAS_db_setup.sh ADMIN_USER" (where ADMIN_USER is replaced with a user that has GRANT access (locally at the command line- e.g. root) and can create tables).
This will create a database called ubertool, create a user ubertool (with password of ubertool), and create and populate a table called CAS in the ubertool db.
