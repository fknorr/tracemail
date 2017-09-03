import psycopg2 as postgres
from .config import Config


class DatabaseError(Exception):
    pass

class Tracemail:
    def __init__(self, config):
        try:
            self._db = postgres.connect('host={} dbname={} user={} password={}'.format(
                config.database.host, config.database.dbname, config.database.user,
                config.database.password))
        except postgres.Error as e:
            raise DatabaseError(e)

    def list_aliases(self):
        try:
            cur = self._db.cursor()
            cur.execute('SELECT * FROM trace_aliases')
            table = cur.fetchall()
            cur.close()
        except postgres.Error as e:
            raise DatabaseError(e)
        return table

    def new_alias(self, alias, mailbox, purpose):
        try:
            cur = self._db.cursor()
            cur.execute('INSERT INTO trace_aliases (alias, mailbox, purpose) VALUES (%s, %s, %s)',
                    (alias, mailbox, purpose))
            cur.close()
            self._db.commit()
        except postgres.Error as e:
            if isinstance(e, postgres.IntegrityError):
                if 'duplicate key' in str(e):
                    raise DatabaseError('Alias already exists')
            raise DatabaseError(e)

    def enable_alias(self, alias, enable):
        pass

