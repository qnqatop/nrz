import app.config.db.db_connection as conn
from app.model.nrz_model.triger_table import TriggerTable
from app.service.srz.srz_logic_update import subscription_logic_update, users_logic_update
from app.service.srz.srz_logic_insert import subscription_logic_insert, users_logic_insert
import os


def srz_scaner():
    """
    просмотр старой таблицы из СРЗ
    :return:
    """

    nrz = conn.MysqlConnection(host=os.environ.get('NRZ_HOST'), port=os.environ.get('NRZ_PORT'),
                               user=os.environ.get('NRZ_USER'), password=os.environ.get('NRZ_PASS'),
                               base=os.environ.get('NRZ_BASE'))
    redis = conn.RedisConnection(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'),
                                 db=os.environ.get('REDIS_DB'))
    srz = conn.MysqlConnection(host=os.environ.get('SRZ_HOST'), port=os.environ.get('SRZ_PORT'),
                               user=os.environ.get('SRZ_USER'), password=os.environ.get('SRZ_PASS'),
                               base=os.environ.get('SRZ_BASE'))

    new_rows = srz.get_no_sync(TriggerTable)

    for row in new_rows:
        if row.table_name == 'users':
            if row.trigger_name == 'after_user_insert':
                users_logic_insert(row, redis, nrz, srz)
            elif row.trigger_name == 'before_update_users':
                users_logic_update(row, nrz, srz, redis)
        elif row.table_name == 'request_shipping':
            if row.trigger_name == 'before_update_subscriptions':
                subscription_logic_update(row, nrz, srz, redis)
            elif row.trigger_name == 'after_subscriptions_insert':
                subscription_logic_insert(row, redis, nrz, srz)
