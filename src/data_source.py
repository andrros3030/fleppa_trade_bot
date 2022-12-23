import ydb
from logger import Logger, blue_color


class DataSource:
    _driver: ydb.Driver
    _pool: ydb.SessionPool
    _logger: Logger

    def __init__(self, ydb_endpoint: str, ydb_database: str, logger: Logger):  #  access_token: str,
        _driver = ydb.Driver(
            endpoint=ydb_endpoint,
            database=ydb_database,
            # credentials=ydb.AuthTokenCredentials(access_token)
        )
        _driver.wait(fail_fast=True, timeout=10)
        _pool = ydb.SessionPool(_driver)
        _logger = logger
        _logger.v("YDB initialization OK", override_color=blue_color())

    def __execute_query(self, session):
        session.transaction()
        # Create the transaction and execute query.
        return session.transaction().execute(
            'select 1 as cnt;',
            commit_tx=True,
            settings=ydb.BaseRequestSettings().with_timeout(5).with_operation_timeout(4)
        )

    def handler(self, command):
        # Execute query with the retry_operation helper.
        result = self._pool.retry_operation_sync(self.__execute_query)
        self._logger.v(str(result), override_color=blue_color())
        return {
            'statusCode': 200,
            'body': str(result[0].rows[0].cnt == 1),
        }
