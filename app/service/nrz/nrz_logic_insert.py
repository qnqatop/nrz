from app.model.nrz_model.user_model import UserNRZ as nrz_user, UserOccupation as nrz_user_occupation, \
    UserConfirmStatus as nrz_user_confirm_status
from app.model.nrz_model.triger_table import TriggerTable
from app.dto.user import nrz_to_srz
from app.dto.subscription import nrz_to_srz as subscription_nrz_to_srz
from app.model.nrz_model.user_model import SubscriptionNRZ as nrz_subscription


def user_after_insert(row, redis, nrz, srz):
    value = redis.get_by_key(f'user_srz_to_nrz_{row.record_id}')
    if value is not None:
        srz_row = srz.get_trigger_row_by_rec_id(value, 'users', 'after_user_insert', TriggerTable)
        nrz.update_sync_status(row)
        srz.update_sync_status(srz_row)
        redis.remove(f'user_srz_to_nrz_{row.record_id}')
    else:
        user = nrz.get_row_by_table_and_id(row.record_id, nrz_user)
        user_occup = nrz.get_row_by_table_and_id(user.occupation_id, nrz_user_occupation)
        user_conf = nrz.get_row_by_table_and_id(user.confirm_status_id, nrz_user_confirm_status)
        srz_user_dto = nrz_to_srz(user, user_occup, user_conf)
        created_nrz_to_srz_user = srz.create_record(srz_user_dto)
        nrz.update_old_id_in_model(user, created_nrz_to_srz_user.id)
        redis.add(f'user_nrz_to_srz_{created_nrz_to_srz_user.id}', user.id)


def subscription_after_insert(row, redis, nrz, srz):
    with nrz.Session() as nrz_session, srz.Session() as srz_session:
        value = redis.get_by_key(f'subscription_srz_to_nrz_{row.record_id}')
        if value is not None:
            srz_row = srz.get_trigger_row_by_rec_id(value, 'request_shipping', 'after_subscriptions_insert', TriggerTable)
            nrz.update_sync_status(row)
            srz.update_sync_status(srz_row)
            redis.remove(f'subscriptions_srz_to_nrz_{row.record_id}')
        else:
            subscription = nrz.get_row_by_table_and_id(row.record_id, nrz_subscription, session=nrz_session)
            user = nrz.get_row_by_table_and_id(subscription.user_id, nrz_user, session=nrz_session)
            srz_sub_dto = subscription_nrz_to_srz(user, subscription)
            created_nrz_to_srz_sub = srz.create_record(srz_sub_dto)
            nrz.update_old_id(subscription,created_nrz_to_srz_sub.id)
            redis.add(f'subscription_nrz_to_srz_{created_nrz_to_srz_sub.id}', subscription.id)


