import app.config.db.db_connection as conn
from app.model.srz_model.user_model import UserSRZ as srz_user
from app.model.nrz_model.triger_table import TriggerTable
from app.dto.user import srz_to_nrz
import os

def srz_scaner():
    """
    просмотр старой таблицы из СРЗ
    :return:
    """

    nrz = conn.MysqlConnection(host=os.environ.get('NRZ_HOST'), port=os.environ.get('NRZ_PORT'), user=os.environ.get('NRZ_USER'), password=os.environ.get('NRZ_PASS'), base=os.environ.get('NRZ_BASE'))
    redis = conn.RedisConnection(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'), db=os.environ.get('REDIS_DB'))
    srz = conn.MysqlConnection(host=os.environ.get('SRZ_HOST'), port=os.environ.get('SRZ_PORT'), user=os.environ.get('SRZ_USER'), password=os.environ.get('SRZ_PASS'), base=os.environ.get('SRZ_BASE'))

    new_rows = srz.get_by_table_and_no_sync(TriggerTable, 'users')

    for row in new_rows:
        value = redis.get_by_key(f'user_nrz_to_srz_{row.record_id}')
        if value is not None:
            nrz_row = nrz.get_trigger_row_by_rec_id(value, TriggerTable)
            srz.update_sync_status(row)
            nrz.update_sync_status(nrz_row)
            redis.remove(f'user_nrz_to_srz_{row.record_id}')
        else:
            user = srz.get_row_by_table_and_id(row.record_id, srz_user)
            if user.occupation == 4:
                occupation_id = 2
            else:
                occupation_id = 1

            if user.confirm == 1:
                confirm_id = 2
            else:
                confirm_id = 1
            nrz_user_dto = srz_to_nrz(user, occupation_id, confirm_id)
            create_srz_to_nrz_user = nrz.create_record(nrz_user_dto)
            redis.add(f'user_srz_to_nrz_{create_srz_to_nrz_user.id}', user.id)
