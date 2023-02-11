from src.common_modules.run_context import global_context
from src.common_modules.data_source import DataSource
from src.base_modules.logger import Logger


global_context.set_testing_mode()
database = DataSource(auth_context=global_context.db_auth_context, logger=Logger(is_poduction=False))
res2 = database.unsafe_exec('SELECT * from t_users')
print(res2)
assert res2 is not None  # проверяем что БД возвращает хоть что-то
assert database.is_admin('439133935') is True  # проверяем, что Андрей - админ
