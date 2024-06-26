from sqlalchemy import Column, Integer, Boolean, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserSRZ(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String)
    password = Column(String)
    last_in = Column(DateTime)
    name = Column(String)
    admin = Column(Integer)
    activ = Column(Boolean)
    generate = Column(String)
    is_provider = Column('isProvider', Boolean)
    role = Column(Integer)
    confirm = Column(Boolean)
    company = Column(String)
    email = Column(String)
    skype = Column(String)
    occupation = Column(Integer)
    status_id = Column('status_id', Integer)
    balance = Column(DECIMAL)
    status_expiry = Column('status_expiry', DateTime)
    show_nat_services = Column('show_nat_services', Boolean)
    working_with_nds = Column('working_with_nds', Boolean)
    company_id = Column('company_id', Integer)
    place = Column('place', String)
    place_code = Column('place_code', String)
    region = Column('region', String)
    region_code = Column('region_code', String)
    rating = Column('rating', Integer)
    has_docs = Column('has_docs', Boolean)
    forum_blocked = Column('forum_blocked', Boolean)
    forum_blocked_expiry = Column('forum_block_expiry', DateTime)
    token_http = Column('token_http', String)
    old_id = Column('old_id', Integer)

    requests = relationship("SubscriptionSRZ", back_populates="user")

class UserRating(Base):
    __tablename__ = 'user_rating'

    user_id = Column('user_id',Integer, primary_key=True)
    reg_rating = Column('reg_rating',DECIMAL)
    reg_date = Column('reg_date',DateTime)
    reg_days = Column('reg_days',Integer)
    data_rating = Column('data_rating',DECIMAL)
    data_has_name = Column('data_has_name',Boolean)
    data_has_docs = Column('data_has_docs',Boolean)
    data_name_equals = Column('data_name_equals',Boolean)
    payment_rating = Column('payment_rating',DECIMAL)
    payment_has_rating = Column('payment_has_rating',Boolean)
    payment_has_subscription = Column('payment_has_subscription',Boolean)
    payment_last_date = Column('payment_last_date',DateTime)
    payment_days = Column('payment_days',Integer)
    timestamp = Column('timestamp',DateTime)


class SubscriptionSRZ(Base):
    __tablename__ = 'request_shipping'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_create = Column(DateTime)
    old_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserSRZ", back_populates="requests")
    status_id = Column(Integer)
    date_close = Column(DateTime)
    region_load_kladr_code = Column(String)
    locality_load_kladr_code = Column(String)
    stevedore_id = Column(Integer)
    culure_id = Column(Integer)
    trader_id = Column(Integer)
    price = Column(Integer)
    weight = Column(Integer)
    scale = Column(Integer)
    load_type_id = Column(Integer)
    where_calculation = Column(String)
    distance = Column(Integer)
    date_load = Column(DateTime)
    region_load_text = Column(String)
    description = Column(String)
    auction = Column(Boolean)
    locality_unload_kladr_code = Column(String)
    region_unload_text = Column(String)
    date_force_closed = Column(DateTime)
    can_call = Column(Integer)
    view_count = Column(Integer)
    up = Column(Integer)
    lat = Column(Integer)
    lon = Column(Integer)
    downtime = Column(String)
    shortage = Column(String)
    culture = Column(String)
    trader = Column(String)
    stevedore = Column(String)
    load_type = Column(String)
    answers_count = Column(Integer)
    is_cargill = Column(Boolean)
    user_access_cargill = Column(Boolean)
    is_potok = Column(Boolean)
    sender_text = Column(String)
