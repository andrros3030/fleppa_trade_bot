"""
Модуль для работы с базой данных
NO PROJECT IMPORTS EXCEPT BASE_MODULES
"""
import psycopg2
import uuid

from src.base_modules.constants import START_MESSAGE
from src.base_modules.logger import Logger
from src.base_modules.routes import DEFAULT_ROUTE, ParsedRoute
from src.base_modules.db_auth_context import DBAuthContext


def _brackets_handler(query: str):
    """
    Функция для правильной работы с кавычками

    :param query: текст запроса с потенциальными нарушениями синтаксиса

    :return: корректный запрос для SQL и его параметры
    """
    query = query.lower().replace('“', "'").replace('”', "'").replace("‘", "'").replace("’", "'")
    return query


class DataSource:
    """
    Класс для работы с базой данных pg sql.

    Функции, вставляющие данные могут принимать как числовые, так и строковые параметры.

    Функции, делающие выборку или обновляющие данные должны принимать параметры в тех типах, которые исходят от БД.
    """
    def __init_connection(self):
        """
        Перезапускает подключение к базе данных используя контекст авторизации
        """
        self.conn = psycopg2.connect(self.auth_context.get_config)
        self.logger.v('Connection to DB set up')

    def __init__(self, logger: Logger, auth_context: DBAuthContext):
        """
        :param logger: логер для записи логов

        :param auth_context: контекст авторизации в базе данных
        """
        self.auth_context = auth_context
        self.conn = None
        self.logger = logger
        self.__init_connection()

    def __make_query(self, query: str, params=None):
        """
        Функция для работы с базой данных, обрабатывающая внутри запрос и ошибки, которые могут выстрелить

        :param query: текст SQL запроса

        :param params: параметры SQL запроса

        :return: результат запроса к БД
        """
        query = _brackets_handler(query)
        try:
            self.logger.v('Starting query from connection: ' + str(self.conn))
            q = self.conn.cursor()
            self.logger.v('Got cursor, executing query: ' + query)
            q.execute(query, params)
            self.logger.v('Query OK, committing')
            self.conn.commit()
            if q.statusmessage.split()[0] in ['INSERT', 'UPDATE', 'DELETE']:
                return q.statusmessage
            return q.fetchall()
        except Exception as error:
            self.logger.e("DB_ERROR: " + str(error))
            self.__init_connection()
            return None

    def __error_handler(self, error):
        """
        Обработчик ошибок логики. Эта функция должна вызываться если не удаётся обработать ответ БД
        (пустой ответ, пропуски в полях и т. д.)

        :param error: выстрелившая ошибка
        """
        self.logger.w("DB_LOGIC: " + str(error))

    def unsafe_exec(self, query: str):
        """
        Команда не для использования внутри бизнес логики!!!
        Предназначена лишь для доступа к базе из телеграм бота администраторами

        :param query: Запрос к базе данных

        :return: результат запроса к БД
        """
        return self.__make_query(query=query)

    def save_user(self, user_id, involve_link: str):
        if involve_link is not None:
            querry = "INSERT INTO T_USERS (pk_id, fk_involve) values(%s, %s) ON CONFLICT DO NOTHING;"
            return self.__make_query(querry, params=(str(user_id), involve_link))
        querry = "INSERT INTO T_USERS (pk_id) values(%s) ON CONFLICT DO NOTHING;"
        return self.__make_query(querry, params=(user_id,))

    def is_admin(self, user_id):
        query = "SELECT l_admin from t_users where pk_id = %s"
        result = self.__make_query(query, params=(str(user_id),))
        try:
            if len(result) == 0:
                return False
            return result[0][0]
        except Exception as e:
            self.logger.e(str(e))
            return False

    def is_banned(self, user_id):
        query = "SELECT l_banned from t_users where pk_id = %s"
        result = self.__make_query(query, params=(str(user_id),))
        try:
            if len(result) == 0:
                return False
            return result[0][0]
        except Exception as e:
            self.logger.e(str(e))
            return False

    def set_route(self, user_id, route=DEFAULT_ROUTE):
        query = "UPDATE t_users SET v_position = %s WHERE pk_id = %s"
        result = self.__make_query(query, params=(route, str(user_id),))
        try:
            if len(result) == 0:
                return False
            return result[0][0]
        except Exception as e:
            self.logger.e(str(e))
            return False

    def __get_current_route(self, user_id) -> str:
        query = "SELECT v_position from t_users where pk_id = %s"
        result = self.__make_query(query, params=(user_id,))
        try:
            if len(result) == 0:
                return DEFAULT_ROUTE
            return result[0][0]
        except Exception as e:
            self.logger.e(str(e))
            return DEFAULT_ROUTE

    def get_current_route(self, user_id) -> ParsedRoute:
        route = self.__get_current_route(str(user_id))
        self.logger.v('Got route ' + str(route) + ' for user ' + str(user_id))
        return ParsedRoute(route)

    def save_feedback_origin(self, user_id, origin_message_id, forwarded_message_id):
        link_id = str(uuid.uuid4())
        query = "INSERT INTO t_feedback (pk_id, fk_user, v_message_id, v_forwarded_id) " \
                "values(%s, %s, %s, %s);"
        return self.__make_query(query,
                                 params=(link_id, str(user_id), str(origin_message_id), str(forwarded_message_id))
                                 )

    def resolve_feedback(self, user_id, origin_message_id, forwarded_message_id):
        user_id = str(user_id)
        origin_message_id = str(origin_message_id)
        forwarded_message_id = str(forwarded_message_id)
        query = "UPDATE t_feedback SET l_answered=true, ts_answered=current_timestamp " \
                "where fk_user=%s and v_message_id=%s and v_forwarded_id=%s"
        return self.__make_query(query, params=(user_id, origin_message_id, forwarded_message_id))

    def get_resolve_time(self, author_id, forwarded_message_id):
        author_id = str(author_id)
        forwarded_message_id = str(forwarded_message_id)
        query = "SELECT ts_answered, ts_requested FROM t_feedback where v_forwarded_id=%s and fk_user=%s"
        result = self.__make_query(query, params=(forwarded_message_id, author_id))
        try:
            if len(result) == 0:
                return None
            diff = result[0][0] - result[0][1]
            return diff.total_seconds()
        except Exception as e:
            self.logger.e(str(e))
            return None

    def get_feedback_origin(self, forwarded_message_id, author_id):
        # TODO: переписать логику на pk_id
        query = "SELECT v_message_id FROM t_feedback where v_forwarded_id=%s and fk_user=%s"
        result = self.__make_query(query, params=(str(forwarded_message_id), str(author_id)))
        try:
            if len(result) == 0:
                return None
            return result[0][0]
        except Exception as e:
            self.logger.e(str(e))
            return None

    def set_admin(self, user_id: str):
        querry = "INSERT INTO T_USERS (pk_id, l_admin) values(%s, true) on conflict (pk_id) do update set l_admin=true"
        return self.__make_query(querry, params=(user_id,))

    def generate_link(self, description: str, startup_message: str):
        link_id = str(uuid.uuid4())
        if startup_message is None:
            querry = "INSERT INTO T_INVOLVE (pk_id, v_desc) values(%s, %s);"
            res = self.__make_query(querry, params=(link_id, description))
        else:
            querry = "INSERT INTO T_INVOLVE (pk_id, v_desc, v_override_start_message) values(%s, %s, %s);"
            res = self.__make_query(querry, params=(link_id, description, startup_message))
        if res is None:
            return res
        return link_id

    def get_start_message(self, start_link: str = None) -> str:
        msg = START_MESSAGE
        self.logger.v('Trying to get start message for link: ' + str(start_link))
        if start_link is not None:
            try:
                result = self.__make_query(
                    query='SELECT v_override_start_message FROM T_INVOLVE WHERE pk_id = %s',
                    params=(start_link,),
                )
                if result is None or len(result) == 0 or len(result[0]) == 0:
                    raise Exception(f'Invalid link or error in reading from DB: {start_link}')
                result = result[0][0]
                if result is not None:
                    self.logger.v(f'Returning message: {result}')
                    return result
            except Exception as e:
                self.__error_handler(e)
        self.logger.v('Returning default message')
        return msg

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
