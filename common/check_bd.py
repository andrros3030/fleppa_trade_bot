import datetime

import psycopg2
from datetime import datetime, timezone
from src.constants import DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_USER_PASSWORD

conn = psycopg2.connect(f"""
    host={DB_HOST}
    port={DB_PORT}
    dbname={DB_NAME}
    user={DB_USER}
    password={DB_USER_PASSWORD}
    target_session_attrs=read-write
""")
# sslmode = verify - full

q = conn.cursor()

dt = datetime.now(timezone.utc)
q.execute(f"insert into t_users (pk_id, l_admin, t_reg) values ('test2', false, '{dt}')")

q.execute('SELECT * from t_users')
conn.commit()
print(q.fetchall())

conn.close()
