import psycopg2


# TODO: почитать про   sslmode=verify-full
class DataSource:
    def __init__(self, host, port, dbname, user, password):
        self.conn = psycopg2.connect(f"""
                host={host}
                port={port}
                dbname={dbname}
                user={user}
                password={password}
                target_session_attrs=read-write
            """)

    def exec(self, querry):
        q = self.conn.cursor()
        q.execute(querry)
        return q.fetchone()

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
