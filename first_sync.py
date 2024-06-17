import os
import time

import app.config.db.db_connection as conn
from app.model.srz_model.user_model import  UserSRZ as user_srz
from dotenv import load_dotenv
from app.dto.user import srz_to_nrz


load_dotenv()



def get_users_by_srz() ->[]:
    srz = conn.MysqlConnection(host=os.environ.get('SRZ_HOST'), port=os.environ.get('SRZ_PORT'),
                               user=os.environ.get('SRZ_USER'), password=os.environ.get('SRZ_PASS'),
                               base=os.environ.get('SRZ_BASE'))
    nrz = conn.MysqlConnection(host=os.environ.get('NRZ_HOST'), port=os.environ.get('NRZ_PORT'), user=os.environ.get('NRZ_USER'), password=os.environ.get('NRZ_PASS'), base=os.environ.get('NRZ_BASE'))


    srz_users = srz.get_table_rows(user_srz)
    i=1
    for user in srz_users:
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
        ##по сути тут должна быть логика обновления id в srz потому что сейчас там нет таких столбцов
        srz.update_old_id_in_model(user,create_srz_to_nrz_user.id)
        print(f'добавлено - {i}')
        i+=1

# get_users_by_srz()