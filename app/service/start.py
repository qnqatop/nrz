import app.config.db.dn_connection as conn


nrz = conn.MysqlConnection(host='127.0.0.1',port=33061, user='root', password='webant',base='base')
print(nrz.get_row_by_table_and_id(1,'users'))
# srz = conn.MysqlConnection(host='127.0.0.1',port=33061, user='root', password='webant',base='base')
# nrzcursor = nrz.cnx.cursor()
# nrzcursor.execute('SELECT * FROM users')
# nrz_users_result = nrzcursor.fetchall()
#
# for x in nrz_users_result:
#     print(type(x))
# nrz.close()


# ###
# сначала идем по тригерам юзеров( тригеры которые не синзронизированы)
#
#
# берем через цикл тригеры и идем в таблицу юзера по id
#     сначала идем в redis и смотрим нет ли там уже сохраненной модели,
#     если есть то подтверждаем синхру и удаляем из редиса
#
# получаем юзера, преобразуем в модель для противоположной базы и сохраняем в нее,
#
# после чего фиксируем ту же модель в redis для того что бы не было зацикливания постоянного
# #-------------------------------------------------------------------
# потом по другим