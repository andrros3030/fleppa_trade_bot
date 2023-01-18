import psycopg2
import uuid
from src.logger import Logger
from src.routes import DEFAULT_ROUTE, ParsedRoute


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
            if q.statusmessage.split()[0] in ['INSERT', 'UPDATE', 'DELETE']:
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

    def save_user(self, user_id: str, involve_link: str):
        if involve_link is not None:
            querry = "INSERT INTO T_USERS (pk_id, fk_involve) values(%s, %s) ON CONFLICT DO NOTHING;"
            return self.__make_querry(querry, params=(user_id, involve_link))
        querry = "INSERT INTO T_USERS (pk_id) values(%s) ON CONFLICT DO NOTHING;"
        return self.__make_querry(querry, params=(user_id,))

    def is_admin(self, user_id):
        if type(user_id) is int:
            querry = "SELECT l_admin from t_users where pk_id = '%s'"
        else:
            querry = "SELECT l_admin from t_users where pk_id = %s"
        result = self.__make_querry(querry, params=(user_id,))
        try:
            if len(result) == 0:
                return False
            return result[0][0]
        except Exception as e:
            self.logger.e(str(e))
            return False

    def is_banned(self, user_id):
        if type(user_id) is int:
            querry = "SELECT l_banned from t_users where pk_id = '%s'"
        else:
            querry = "SELECT l_banned from t_users where pk_id = %s"
        result = self.__make_querry(querry, params=(user_id,))
        try:
            if len(result) == 0:
                return False
            return result[0][0]
        except Exception as e:
            self.logger.e(str(e))
            return False

    def set_route(self, user_id, route=DEFAULT_ROUTE):
        if type(user_id) is int:
            querry = f"UPDATE t_users SET v_position='{route}' WHERE pk_id = '%s'"
        else:
            querry = f"UPDATE t_users SET v_position='{route}' WHERE pk_id = %s"
        result = self.__make_querry(querry, params=(user_id,))
        try:
            if len(result) == 0:
                return False
            return result[0][0]
        except Exception as e:
            self.logger.e(str(e))
            return False

    def __get_current_route(self, user_id) -> str:
        if type(user_id) is int:
            querry = "SELECT v_position from t_users where pk_id = '%s'"
        else:
            querry = "SELECT v_position from t_users where pk_id = %s"
        result = self.__make_querry(querry, params=(user_id,))
        try:
            if len(result) == 0:
                return DEFAULT_ROUTE
            return result[0][0]
        except Exception as e:
            self.logger.e(str(e))
            return DEFAULT_ROUTE

    def get_current_route(self, user_id) -> ParsedRoute:
        route = self.__get_current_route(user_id)
        self.logger.v('Got route ' + str(route) + ' for user ' + str(user_id))
        return ParsedRoute(route)

    def save_feedback_origin(self, user_id, origin_message_id, forwarded_message_id):
        link_id = str(uuid.uuid4())
        querry = "INSERT INTO t_feedback (pk_id, fk_user, v_message_id, v_forwarded_id) " \
                 "values(%s, %s, %s, %s);"
        return self.__make_querry(querry, params=(link_id, user_id, origin_message_id, forwarded_message_id))

    def get_feedback_origin(self, forwarded_message_id, author_id):
        if type(author_id) is int:
            querry = "SELECT v_message_id FROM t_feedback where v_forwarded_id='%s' and fk_user='%s'"
        else:
            querry = "SELECT v_message_id FROM t_feedback where v_forwarded_id=%s and fk_user=%s"
        result = self.__make_querry(querry, params=(forwarded_message_id, author_id))
        try:
            if len(result) == 0:
                return None
            return result[0][0]
        except Exception as e:
            self.logger.e(str(e))
            return None

    def set_admin(self, user_id: str):
        querry = "INSERT INTO T_USERS (pk_id, l_admin) values(%s, true) on conflict (pk_id) do update set l_admin=true"
        return self.__make_querry(querry, params=(user_id,))

    def generate_link(self, description: str, startup_message: str) -> str:
        link_id = str(uuid.uuid4())
        if startup_message is None:
            querry = "INSERT INTO T_INVOLVE (pk_id, v_desc) values(%s, %s) on conflict (pk_id) do nothing;"
            self.__make_querry(querry, params=(link_id, description))
        else:
            querry = "INSERT INTO T_INVOLVE (pk_id, v_desc, v_override_start_message) " \
                     "values(%s, %s, %s) on conflict (pk_id) do nothing;"
            self.__make_querry(querry, params=(link_id, description, startup_message))
        return link_id

    def get_start_message(self, start_link: str = None) -> str:
        msg = 'Здарова, скоро тут будет супер трейд стратегия от Шлеппы, ' \
               'а пока - держи мой пульс ' \
               'https://www.tinkoff.ru/invest/social/profile/fleppa_war_crimes_fa?utm_source=share'
        self.logger.v('Trying to get start message for link: ' + str(start_link))
        if start_link is not None:
            try:
                return self.__make_querry(
                    querry='SELECT v_override_start_message FROM T_INVOLVE WHERE pk_id = %s',
                    params=(start_link,),
                )[0]
            except Exception as e:
                self.logger.e(str(e))
            finally:
                pass
        return msg

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
