import psycopg2
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
q.execute('SELECT * from t_users')

print(q.fetchone())

conn.close()
