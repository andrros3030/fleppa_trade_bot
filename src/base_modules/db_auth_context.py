"""
Контекст для авторизации в базе данных
NO PROJECT IMPORTS IN THIS FILE
"""


class DBAuthContext:
    """
    Контекст для авторизации в базе данных
    """
    def __init__(self, on_error):
        self.user = None
        self.password = None
        self.host = None
        self.port = None
        self.is_prod = None
        self.database = None
        self.dbname = None
        self.on_error = on_error

    def fill(self, user: str = None, password: str = None,
             host: str = None, port: str = None, is_prod: bool = None, dbname: str = None):
        self.user = user
        self.password = password
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.is_prod = is_prod
        # TODO: посмотреть на логику, кажется она избыточна
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
