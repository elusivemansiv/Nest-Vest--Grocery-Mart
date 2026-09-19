from django.db.backends.signals import connection_created


def disable_foreign_keys(sender, connection, **kwargs):
    """
    Disable SQLite foreign key enforcement.

    Django handles cascading deletes (CASCADE, SET_NULL, etc.) in Python code,
    so SQLite's own FK enforcement is redundant. When the DB has legacy tables
    (e.g. django_admin_log referencing auth_user instead of the custom
    userauths_user), SQLite's enforcement incorrectly blocks valid deletions.
    """
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = OFF;')


connection_created.connect(disable_foreign_keys)
