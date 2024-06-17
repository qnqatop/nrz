from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class UserNRZ(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String)
    last_name = Column(String)
    first_name = Column(String)
    occupation_id = Column(Integer)
    organization_name = Column(String)
    is_verified_organization = Column(Boolean)
    password = Column(String)
    confirm_status_id = Column(Integer)
    online_at = Column(DateTime)
    avatar = Column(String)
    old_id = Column(Integer)
    disabled_at = Column(DateTime)
    is_first_account_with_this_number = Column(Boolean)
    is_disabled_push_notifications = Column(Boolean)
    is_privacy_policy_accepted = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class UserConfirmStatus(Base):
    __tablename__ = 'user_confirm_statuses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)

class UserOccupation(Base):
    __tablename__ = 'user_occupations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)

class UserForumAdmin(Base):
    __tablename__ = 'user_forum_admins'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)

class SubscriptionNRZ(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    type_id = Column(Integer)
    loading_region = Column(String)
    loading_locality = Column(String)
    load_kladr_code = Column(String)
    old_id = Column(Integer)
    longitude = Column(Integer)
    latitude = Column(Integer)
    stevedore_id = Column(Integer, ForeignKey('stevedores.id'))
    loaded_at = Column(DateTime)
    closed_at = Column(DateTime)
    distance = Column(Integer)
    culture_id = Column(Integer, ForeignKey('application_cultures.id'))
    transportation_price = Column(Integer)
    load_capacity = Column(Integer)
    load_type_id = Column(Integer, ForeignKey('application_load_types.id'))  # Внешний ключ
    load_size = Column(Integer)
    is_fixed_price = Column(Boolean)
    downtime_payment_form = Column(String)
    acceptable_shortage = Column(String)
    additional_info = Column(String)
    payment_type_id = Column(Integer)
    can_carriers_call_me = Column(Boolean)
    payment_time = Column(String)
    is_dump_trucks_suitable = Column(Boolean)
    is_carrier_work_with_hartiya = Column(Boolean)
    archived_at = Column(DateTime)
    created_at = Column(DateTime)

    # Определение отношений
    stevedore = relationship('StevedoreNRZ')
    culture = relationship('CultureNRZ')
    load_type = relationship('LoadTypeSubNRZ')

class StevedoreNRZ(Base):
    __tablename__ = 'stevedores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String, nullable=False)

class CultureNRZ(Base):
    __tablename__ = 'application_cultures'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)

class LoadTypeSubNRZ(Base):
    __tablename__ = 'application_load_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
