import app.config.db.db_connection as conn
from app.model.nrz_model.user_model import UserNRZ as nrz_user, UserOccupation as nrz_user_occupation, \
    UserConfirmStatus as nrz_user_confirm_status
from app.model.nrz_model.triger_table import TriggerTable
from app.dto.user import nrz_to_srz


def nrz_scaner():
    """
    просмотр новых таблиц из НРЗ
    :return:
    """
    nrz = conn.MysqlConnection(host='127.0.0.1', port=33061, user='root', password='webant', base='base')
    redis = conn.RedisConnection(host='127.0.0.1', port=6379, db=0)
    srz = conn.MysqlConnection(host='127.0.0.1', port=33062, user='superuser', password='webant', base='base')
    new_rows = nrz.get_by_table_and_no_sync(TriggerTable, 'users')

    for row in new_rows:
        value = redis.get_by_key(f'user_srz_to_nrz_{row.record_id}')
        if value is not None:
            srz_row = srz.get_trigger_row_by_rec_id(value, TriggerTable)
            nrz.update_sync_status(row)
            srz.update_sync_status(srz_row)
            redis.remove(f'user_srz_to_nrz_{row.record_id}')
        else:
            user = nrz.get_row_by_table_and_id(row.record_id, nrz_user)
            user_occup = nrz.get_row_by_table_and_id(user.occupation_id, nrz_user_occupation)
            user_conf = nrz.get_row_by_table_and_id(user.confirm_status_id, nrz_user_confirm_status)
            srz_user_dto = nrz_to_srz(user, user_occup, user_conf)
            created_nrz_to_srz_user = srz.create_record(srz_user_dto)
            redis.add(f'user_nrz_to_srz_{created_nrz_to_srz_user.id}', user.id)
