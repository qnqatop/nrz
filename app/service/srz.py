import app.config.db.db_connection as conn
from app.model.srz_model.user_model import UserSRZ as srz_user
from app.model.nrz_model.triger_table import TriggerTable
from app.dto.user import srz_to_nrz


def srz_scaner():
    """
    просмотр старой таблицы из СРЗ
    :return:
    """

    '''
    CREATE USER 'all'@'%' IDENTIFIED BY 'webant';

    GRANT ALL PRIVILEGES ON *.* TO 'all'@'%' WITH GRANT OPTION;

    FLUSH PRIVILEGES;
    '''
    nrz = conn.MysqlConnection(host='127.0.0.1', port=33061, user='root', password='webant', base='base')
    redis = conn.RedisConnection(host='127.0.0.1', port=6379, db=0)
    srz = conn.MysqlConnection(host='127.0.0.1', port=33062, user='superuser', password='webant', base='base')

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

            # INSERT
            # INTO
            # users(login, password, last_in, name, admin, activ, generate, isProvider, role, confirm, company, email,
            #       skype, occupation, status_id, balance, status_expiry, show_nat_services, working_with_nds, company_id,
            #       place, place_code, region, region_code, rating, has_docs, forum_blocked, forum_block_expiry,
            #       token_http)
            # VALUES('+79876543210', 'f5bb0c8de146c67b44babbf4e6584cc0', '2024-05-04 15:59:37', 'Иванов Иван', 1, 1, NULL,
            #        0, 0, 1, 'PortTranzit', NULL, NULL, 4, 1, 0, NULL, 1, 0, 0, NULL, NULL, NULL, NULL, 5, 0, 0, NULL,
            #        'token');
