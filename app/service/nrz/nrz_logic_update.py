from app.model.nrz_model.user_model import UserNRZ as nrz_user, UserOccupation as nrz_user_occupation, \
    UserConfirmStatus as nrz_user_confirm_status
from app.model.nrz_model.triger_table import TriggerTable
from app.dto.user import nrz_to_srz
from app.dto.subscription import nrz_to_srz as subscription_nrz_to_srz
from app.model.nrz_model.user_model import SubscriptionNRZ as nrz_subscription


def users_logic_update(row, nrz, srz,redis):
    with nrz.Session() as nrz_session:
        value = redis.get_by_key(f'update_user_srz_to_nrz_{row.record_id}')
        if value is not None:
            srz_row = srz.get_trigger_row_by_rec_id(value, 'users', 'before_update_users', TriggerTable)
            nrz.update_sync_status(row)
            srz.update_sync_status(srz_row)
            redis.remove(f'update_user_srz_to_nrz_{row.record_id}')
        else:
            user = nrz.get_row_by_table_and_id(row.record_id, nrz_user,session=nrz_session)
            user_occup = nrz.get_row_by_table_and_id(user.occupation_id, nrz_user_occupation,session=nrz_session)
            user_conf = nrz.get_row_by_table_and_id(user.confirm_status_id, nrz_user_confirm_status,session=nrz_session)
            srz_user_dto = nrz_to_srz(user, user_occup, user_conf,True)
            srz.update_record(srz_user_dto)
            redis.add(f'update_user_nrz_to_srz_{srz_user_dto.id}',user.id)


def subscription_logic_update(row, nrz, srz,redis):
    with nrz.Session() as nrz_session:
        value = redis.get_by_key(f'update_subscription_srz_to_nrz_{row.record_id}')
        if value is not None:
            srz_row = srz.get_trigger_row_by_rec_id(value, 'request_shipping', 'before_update_subscriptions',TriggerTable)
            nrz.update_sync_status(row)
            srz.update_sync_status(srz_row)
            redis.remove(f'update_subscription_srz_to_nrz_{row.record_id}')
        else:
            subscription = nrz.get_row_by_table_and_id(row.record_id, nrz_subscription, session=nrz_session)
            user = nrz.get_row_by_table_and_id(subscription.user_id, nrz_user, session=nrz_session)
            srz_sub_dto = subscription_nrz_to_srz(user, subscription,True)
            srz.update_record(srz_sub_dto)
            redis.add(f'update_subscription_nrz_to_srz_{srz_sub_dto.id}', subscription.id)
