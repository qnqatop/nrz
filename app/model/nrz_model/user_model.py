from sqlalchemy import Column, Integer, String, Boolean,DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserNRZ(Base):
    __tablename__ = 'users'

    id =  Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String)
    last_name = Column(String)
    first_name = Column(String)
    occupation_id = Column('occupation_id',Integer)
    organization_name = Column('organization_name',String)
    is_verified_organization = Column('is_verified_organization',Boolean)
    password = Column(String)
    confirm_status_id = Column('confirm_status_id',Integer)
    online_at = Column('online_at',DateTime)
    avatar = Column('avatar',String)
    old_id = Column('old_id',Integer)
    disabled_at = Column('disabled_at',DateTime)
    is_first_account_with_this_number = Column('is_first_account_with_this_number',Boolean)
    is_disabled_push_notifications = Column('is_disabled_push_notifications',Boolean)
    is_privacy_policy_accepted = Column('is_privacy_policy_accepted',Boolean)
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
    user_id = Column('user_id',Integer)