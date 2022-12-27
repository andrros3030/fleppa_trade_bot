import psycopg2
from src.logger import Logger
from src.constants import global_context


# TODO: почитать про   sslmode=verify-full
class DataSource:
    def init_connection(self):
        if global_context.IS_PRODUCTION:
            self.conn = psycopg2.connect(
                database=self.host.split('.')[0],  # Идентификатор подключения
                user=self.user,  # Пользователь БД
                password=self.password,
                host=self.host,  # Точка входа
                port=self.port,
                sslmode="require",
            )
            # context.token["access_token"]
            # akflka8fhhde7dkske86
        else:
            self.conn = psycopg2.connect(f"""
                                   host={self.host}
                                   port={self.port}
                                   dbname={self.dbname}
                                   user={self.user}
                                   password={self.password}
                                   target_session_attrs=read-write
                               """)
        self.logger.v('Connection to DB set up')

    def __init__(self,  logger: Logger, host: str = None, port: str = None, dbname: str = None, user: str = None,
                 password: str = None,):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.conn = None
        self.logger = logger
        self.init_connection()

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
        querry = querry.replace('“', "'").replace('”', "'").replace("‘", "'").replace("’", "'")
        try:
            self.logger.v('Starting querry from connection: ' + str(self.conn))
            q = self.conn.cursor()
            self.logger.v('Got cursor, executing querry: ' + querry)
            q.execute(querry)
            self.logger.v('Querry OK, commiting')
            self.conn.commit()
            if q.statusmessage.split()[0] == 'INSERT':
                return q.statusmessage
            return q.fetchall()
        except Exception as e:
            return self.__error_handler(e)

    def save_user(self, user_id: str):
        try:
            self.logger.v('Saving user with id ' + user_id)
            # TODO: implement insert into DB + check if not exists
            pass
        except Exception as e:
            return self.__error_handler(e)

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
