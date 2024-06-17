from app.model.nrz_model.user_model import UserNRZ
from app.model.srz_model.user_model import UserSRZ
from app.model.srz_model.user_model import SubscriptionSRZ
from app.model.nrz_model.user_model import SubscriptionNRZ
from datetime import datetime


def nrz_to_srz(nrz_user: UserNRZ,nrz_sub: SubscriptionNRZ,update = False) -> SubscriptionSRZ:
    srz_sub = SubscriptionSRZ()
    if update:
        srz_sub.id = nrz_sub.old_id
    srz_sub.date_create = datetime.now()
    srz_sub.user_id = nrz_user.old_id
    srz_sub.status_id = 1
    srz_sub.date_close = nrz_sub.closed_at
    srz_sub.region_load_text = nrz_sub.load_kladr_code[0:2]
    srz_sub.locality_load_kladr_code = nrz_sub.load_kladr_code

    srz_sub.stevedore = nrz_sub.stevedore.name
    srz_sub.culture = nrz_sub.culture.title
    srz_sub.trader = ''
    srz_sub.trader_id = None
    srz_sub.culure_id = nrz_sub.culture_id
    srz_sub.price = nrz_sub.transportation_price
    srz_sub.weight = nrz_sub.load_size
    srz_sub.scale = nrz_sub.load_capacity
    srz_sub.load_type_id = nrz_sub.load_type_id
    srz_sub.where_calculation = nrz_sub.payment_time
    srz_sub.distance = nrz_sub.distance
    srz_sub.date_load = nrz_sub.loaded_at
    srz_sub.region_load_text = nrz_sub.loading_region
    srz_sub.description = nrz_sub.additional_info
    srz_sub.auction = nrz_sub.is_fixed_price
    srz_sub.locality_unload_kladr_code = nrz_sub.load_kladr_code
    try:
        srz_sub.region_unload_text = nrz_sub.stevedore.address
    except:
        srz_sub.region_unload_text = ''
    srz_sub.date_force_closed = None
    srz_sub.can_call = int(nrz_sub.can_carriers_call_me)
    srz_sub.view_count = 0
    srz_sub.up = 0
    srz_sub.lat = nrz_sub.latitude
    srz_sub.lon = nrz_sub.longitude
    srz_sub.downtime = nrz_sub.downtime_payment_form
    srz_sub.shortage = nrz_sub.acceptable_shortage
    srz_sub.stevedore_id = nrz_sub.stevedore_id
    srz_sub.load_type = nrz_sub.load_type.title
    srz_sub.answers_count = 0
    srz_sub.is_cargill = nrz_sub.is_dump_trucks_suitable
    srz_sub.user_access_cargill = nrz_sub.is_carrier_work_with_hartiya
    srz_sub.is_potok = 0
    srz_sub.sender_text = None


    return srz_sub


def srz_to_nrz(srz_user: UserSRZ, srz_sub: SubscriptionSRZ,update = False) -> SubscriptionNRZ:
    nrz_sub = SubscriptionNRZ()

    if update:
        nrz_sub.id = srz_sub.old_id
    nrz_sub.user_id = srz_user.old_id
    nrz_sub.type_id = 1
    try:

        nrz_sub.loading_region = srz_sub.region_load_text.split(',')[0]
        nrz_sub.loading_locality = srz_sub.region_load_text.split(',')[1]
    except:
        nrz_sub.loading_region = srz_sub.region_load_text
        nrz_sub.loading_locality = srz_sub.region_load_text
    nrz_sub.load_kladr_code = srz_sub.locality_load_kladr_code
    nrz_sub.longitude = srz_sub.lon
    nrz_sub.latitude = srz_sub.lat
    nrz_sub.stevedore_id = srz_sub.stevedore_id
    nrz_sub.loaded_at = srz_sub.date_load
    nrz_sub.closed_at = srz_sub.date_close
    nrz_sub.distance = srz_sub.distance
    nrz_sub.culture_id = srz_sub.culure_id
    nrz_sub.transportation_price = srz_sub.price
    nrz_sub.load_capacity = srz_sub.scale
    nrz_sub.load_type_id = srz_sub.load_type_id
    nrz_sub.load_size = srz_sub.weight
    nrz_sub.is_fixed_price = srz_sub.auction
    nrz_sub.downtime_payment_form = srz_sub.downtime
    nrz_sub.acceptable_shortage = srz_sub.shortage
    nrz_sub.additional_info = srz_sub.description
    nrz_sub.payment_type_id = 1
    nrz_sub.can_carriers_call_me = srz_sub.can_call
    nrz_sub.payment_time = srz_sub.where_calculation
    nrz_sub.is_dump_trucks_suitable = srz_sub.is_cargill
    nrz_sub.is_carrier_work_with_hartiya = srz_sub.user_access_cargill
    nrz_sub.archived_at = None
    nrz_sub.created_at = srz_sub.date_create
    
    return nrz_sub

