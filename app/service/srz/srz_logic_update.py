from app.model.srz_model.user_model import UserSRZ as srz_user
from app.model.srz_model.user_model import SubscriptionSRZ as srz_subscription
from app.model.nrz_model.triger_table import TriggerTable
from app.dto.user import srz_to_nrz
from app.dto.subscription import srz_to_nrz as subscription_srz_to_nrz


def users_logic_update(row, nrz, srz,redis):
    with srz.Session() as srz_session:
        value = redis.get_by_key(f'update_user_nrz_to_srz_{row.record_id}')
        if value is not None:
            nrz_row = nrz.get_trigger_row_by_rec_id(value, 'users', 'before_update_users', TriggerTable)
            srz.update_sync_status(row)
            nrz.update_sync_status(nrz_row)
            redis.remove(f'update_user_nrz_to_srz_{row.record_id}')
        else:
            user = srz.get_row_by_table_and_id(row.record_id, srz_user,session=srz_session)
            if user.occupation == 4:
                occupation_id = 2
            else:
                occupation_id = 1
            if user.confirm == 1:
                confirm_id = 2
            else:
                confirm_id = 1
            nrz_user_dto = srz_to_nrz(user, occupation_id, confirm_id, True)
            nrz.update_record(nrz_user_dto)
            redis.add(f'update_user_srz_to_nrz_{nrz_user_dto.id}', user.id)


def subscription_logic_update(row, nrz, srz,redis):
    with srz.Session() as srz_session:
        value = redis.get_by_key(f'update_subscription_nrz_to_srz_{row.record_id}')
        if value is not None:
            nrz_row = nrz.get_trigger_row_by_rec_id(value, 'subscriptions', 'before_update_subscriptions', TriggerTable)
            srz.update_sync_status(row)
            nrz.update_sync_status(nrz_row)
            redis.remove(f'update_subscription_nrz_to_srz_{row.record_id}')
        else:
            subscription = srz.get_row_by_table_and_id(row.record_id, srz_subscription,session=srz_session)
            user = srz.get_row_by_table_and_id(subscription.user_id, srz_user,session=srz_session)
            nrz_sub_dto = subscription_srz_to_nrz(user, subscription,True)
            nrz.update_record(nrz_sub_dto)
            redis.add(f'update_subscription_srz_to_nrz_{nrz_sub_dto.id}',subscription.id)
