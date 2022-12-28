from datetime import datetime, timezone
from src.constants import global_context
from src.data_source import DataSource
from src.logger import Logger


global_context.set_testing_mode()
database = DataSource(auth_context=global_context.auth_context, logger=Logger(is_poduction=False))
dt = datetime.now(timezone.utc)
# res1 = database.unsafe_exec(f"insert into t_users (pk_id, l_admin, t_reg) values ('test2', false, '{dt}')")
res2 = database.unsafe_exec('SELECT * from t_users')
# print(res1)
print(res2)
print(database.is_admin('439133935'))
