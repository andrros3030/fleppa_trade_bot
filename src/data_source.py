import psycopg2
from src.logger import Logger


class DBAuthContext:
    def __init__(self, user: str, password: str, host: str, port: str, is_prod: bool, dbname: str = None):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.is_prod = is_prod
        if is_prod:
            self.database = host.split('.')[0]
        else:
            self.dbname = dbname

    @property
    def get_config(self):
        if self.is_prod:
            return f"""
            dbname={self.database}
            host={self.host}
            port={self.port}
            user={self.user}
            password={self.password}
            sslmode=require
            """
        else:
            return f"""
                host={self.host}
                port={self.port}
                dbname={self.dbname}
                user={self.user}
                password={self.password}
                target_session_attrs=read-write
            """


def brackets_handler(querry: str):
    querry = querry.lower().replace('“', "'").replace('”', "'").replace("‘", "'").replace("’", "'")
    return querry


class DataSource:
    def init_connection(self):
        self.conn = psycopg2.connect(self.auth_context.get_config)
        self.logger.v('Connection to DB set up')

    def __init__(self, logger: Logger, auth_context: DBAuthContext):
        self.auth_context = auth_context
        self.conn = None
        self.logger = logger
        self.init_connection()

    def __make_querry(self, querry: str, safe_mode: bool = True, params=None):
        if safe_mode:
            querry = brackets_handler(querry)
        try:
            self.logger.v('Starting querry from connection: ' + str(self.conn))
            q = self.conn.cursor()
            self.logger.v('Got cursor, executing querry: ' + querry)
            q.execute(querry, params)
            self.logger.v('Querry OK, commiting')
            self.conn.commit()
            if q.statusmessage.split()[0] == 'INSERT':
                return q.statusmessage
            return q.fetchall()
        except Exception as e:
            return self.__error_handler(e)

    def __error_handler(self, error):
        self.logger.e(error)
        self.init_connection()
        return error

    def unsafe_exec(self, querry: str):
        """
        Команда не для использования внутри бизнес логики!!!
        Предназначена лишь для доступа к базе из телеграм бота администраторами
        :param querry:
        Запрос к базе данных
        :return:
        """
        return self.__make_querry(querry=querry)

    def save_user(self, user_id: str):
        querry = "INSERT INTO T_USERS (pk_id) values(%s) ON CONFLICT DO NOTHING;"
        return self.__make_querry(querry, params=(user_id,))

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
