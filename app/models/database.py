import psycopg2
import psycopg2.extras


class DataBase:
    __instance = None
    __connection = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, uri):
        if cls.__instance is None:
            cls.__connection = psycopg2.connect(uri, cursor_factory=psycopg2.extras.RealDictCursor)
            cls.__connection.autocommit = True
            cls.__instance = cls.__new__(cls)

            with open('app/models/schema.sql', 'r', encoding='utf-8') as file:
                cls.__instance.execute(file.read())

        return cls.__instance

    def execute(self, sql, args=None):
        with self.__connection.cursor() as cur:
            cur.execute(sql, args)

    def select(self, sql, args=None):
        with self.__connection.cursor() as cur:
            cur.execute(sql, args)
            return [dict(row) for row in cur.fetchall()]

    def get_items(self, server=None):
        if server:
            return self.select('select * from items where server=%s', (server,))
        else:
            return self.select('select * from items')

    def get_item(self, item_id):
        return self.select('select * from items where id=%s', (item_id,))

    def get_users_with_login(self, login):
        return self.select('select * from users where login=%s', (login,))

    def get_users_with_id(self, uid):
        return self.select('select * from users where id=%s', (uid,))

    def create_user(self, login, password):
        self.execute('insert into users (login, password) values (%s, %s)', (login, password))

    def delete_item(self, item_id):
        self.execute('delete from items where id=%s', (item_id, ))

    def add_item(self, name, description, server, pennies_price, photo_filename):
        self.execute("insert into items (name, description, server, penniesPrice, photoFilename) values "
                     "(%s, %s, %s, %s, %s)", (name, description, server, pennies_price, photo_filename))
