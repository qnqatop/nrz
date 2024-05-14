import app.config.db.db_connection as conn
from app.model.nrz_model.user_model import UserNRZ as nrz_user, UserOccupation as nrz_user_occupation, \
    UserConfirmStatus as nrz_user_confirm_status
from app.model.nrz_model.triger_table import TriggerTable
from app.dto.user import nrz_to_srz
import os

def nrz_scaner():
    """
    просмотр новых таблиц из НРЗ
    :return:
    """
    nrz = conn.MysqlConnection(host=os.environ.get('NRZ_HOST'), port=os.environ.get('NRZ_PORT'), user=os.environ.get('NRZ_USER'), password=os.environ.get('NRZ_PASS'), base=os.environ.get('NRZ_BASE'))
    redis = conn.RedisConnection(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'), db=os.environ.get('REDIS_DB'))
    srz = conn.MysqlConnection(host=os.environ.get('SRZ_HOST'), port=os.environ.get('SRZ_PORT'), user=os.environ.get('SRZ_USER'), password=os.environ.get('SRZ_PASS'), base=os.environ.get('SRZ_BASE'))

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
