import time

from app.model.nrz_model.user_model import UserNRZ,UserOccupation,UserConfirmStatus
from app.model.srz_model.user_model import UserSRZ
from datetime import datetime


def nrz_to_srz(nrz_user: UserNRZ,nrz_user_occup: UserOccupation,nrz_user_confirm: UserConfirmStatus) -> UserSRZ:
    srz_user = UserSRZ()
    srz_user.login = nrz_user.phone
    srz_user.password = nrz_user.password
    srz_user.last_in = nrz_user.online_at
    srz_user.name = f'{nrz_user.last_name} {nrz_user.first_name}'
    srz_user.admin = 1
    srz_user.activ = 1
    srz_user.generate = None
    srz_user.is_provider = 0
    srz_user.role = 0
    if nrz_user_confirm.title == 'not_confirmed':
        srz_user.confirm = 0
    elif nrz_user_confirm.title == 'confirmed':
        srz_user.confirm = 1
    else:
        srz_user.confirm = 0
    srz_user.company = nrz_user.organization_name
    srz_user.email = None
    srz_user.skype = None
    if nrz_user_occup.id == 2:
        srz_user.occupation = 4
    else:
        srz_user.occupation = 1
    srz_user.status_id = 1
    srz_user.balance = 0
    srz_user.status_expiry = nrz_user.created_at
    srz_user.show_nat_services = 1
    srz_user.working_with_nds = 0
    srz_user.company_id = 0
    srz_user.place = None
    srz_user.place_code = None
    srz_user.region = None
    srz_user.region_code = None
    srz_user.rating = 5
    srz_user.has_docs = 0
    srz_user.forum_blocked = 0
    srz_user.forum_blocked_expiry = None
    srz_user.token_http = 'token'

    return srz_user

def srz_to_nrz(srz_user: UserSRZ,ocuppation_id,confirm_status_id,) -> UserNRZ:
    nrz_user = UserNRZ()
    nrz_user.phone = srz_user.login
    nrz_user.last_name = srz_user.name.split(' ')[0]
    nrz_user.first_name = srz_user.name.split(' ')[1]
    nrz_user.occupation_id = ocuppation_id
    nrz_user.organization_name = srz_user.company
    nrz_user.is_verified_organization = False
    nrz_user.password = srz_user.password
    nrz_user.confirm_status_id = confirm_status_id
    nrz_user.online_at = srz_user.last_in
    nrz_user.avatar = None
    nrz_user.old_id = srz_user.id
    nrz_user.disabled_at = None
    nrz_user.is_first_account_with_this_number = True
    nrz_user.is_disabled_push_notifications = False
    nrz_user.is_privacy_policy_accepted = True
    nrz_user.created_at = datetime.now()
    nrz_user.updated_at = datetime.now()


    return nrz_user