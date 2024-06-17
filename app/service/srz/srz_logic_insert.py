from app.model.srz_model.user_model import UserSRZ as srz_user
from app.model.srz_model.user_model import SubscriptionSRZ as srz_subscription
from app.model.nrz_model.triger_table import TriggerTable
from app.dto.user import srz_to_nrz
from app.dto.subscription import srz_to_nrz as subscription_srz_to_nrz


def users_logic_insert(row, redis, nrz, srz):
    value = redis.get_by_key(f'user_nrz_to_srz_{row.record_id}')
    if value is not None:
        nrz_row = nrz.get_trigger_row_by_rec_id(value, 'users', 'after_user_insert', TriggerTable)
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
        srz.update_old_id_in_model(user, create_srz_to_nrz_user.id)
        redis.add(f'user_srz_to_nrz_{create_srz_to_nrz_user.id}', user.id)


def subscription_logic_insert(row, redis, nrz, srz):
    value = redis.get_by_key(f'subscription_nrz_to_srz_{row.record_id}')
    if value is not None:
        nrz_row = nrz.get_trigger_row_by_rec_id(value, 'subscriptions', 'after_subscriptions_insert', TriggerTable)
        srz.update_sync_status(row)
        nrz.update_sync_status(nrz_row)
        redis.remove(f'subscription_nrz_to_srz_{row.record_id}')
    else:
        subscription = srz.get_row_by_table_and_id(row.record_id, srz_subscription)
        user = srz.get_row_by_table_and_id(subscription.user_id, srz_user)
        nrz_sub_dto = subscription_srz_to_nrz(user, subscription)
        create_srz_to_nrz_sub = nrz.create_record(nrz_sub_dto)
        redis.add(f'subscription_srz_to_nrz_{create_srz_to_nrz_sub.id}', subscription.id)
