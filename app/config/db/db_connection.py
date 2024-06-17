from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis


class MysqlConnection:
    def __init__(self, host, port, user, password, base):
        self.engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{base}')
        self.Session = sessionmaker(bind=self.engine)

    def close(self):
        self.engine.dispose()

    def get_row_by_table_and_id(self, id, model, session=None):
        if session is None:
            with self.Session() as session:
                return session.get(model, id)
        else:
            return session.get(model, id)

    def update_record(self, model_instance):
        with self.Session() as session:
            # Получаем существующую запись по ID
            existing_record = session.query(model_instance.__class__).filter_by(id=model_instance.id).first()

            if existing_record:
                # Сравниваем и обновляем только измененные атрибуты
                for key, value in model_instance.__dict__.items():
                    if key != '_sa_instance_state' and getattr(existing_record, key) != value:
                        setattr(existing_record, key, value)

                session.commit()
                session.refresh(existing_record)
                return existing_record
            else:
                raise ValueError("Record does not exist.")

    def get_trigger_row_by_rec_id(self,rec_id,table_name,trigger_name,model):
        with self.Session() as session:
            return session.query(model).filter(model.record_id == rec_id).filter(model.trigger_name == trigger_name).filter(model.table_name == table_name).filter(model.is_synced == False).first()
    def get_no_sync(self, model,) -> []:
        with self.Session() as session:
            return session.query(model).filter(model.is_synced == False).all()

    def get_table_rows(self,model):
        with self.Session() as session:
            return session.query(model).all()
    def create_record(self, model_instance):
        with self.Session() as session:
            session.add(model_instance)
            session.commit()
            session.refresh(model_instance)

            return model_instance

    def update_sync_status(self, model):
        with self.Session() as session:
            if isinstance(model, model.__class__):
                session.query(model.__class__).filter(model.__class__.id == model.id).update(
                    {model.__class__.is_synced: True}, synchronize_session=False)
            else:
                raise TypeError("Argument must be an instance of the model class")
            session.commit()

    def update_old_id(self, model,id):
        with self.Session() as session:
            if isinstance(model, model.__class__):
                session.query(model.__class__).filter(model.__class__.id == model.id).update(
                    {model.__class__.old_id: id}, synchronize_session=False)
            else:
                raise TypeError("Argument must be an instance of the model class")
            session.commit()


    def update_model(self,model):
        ##TODO доделить через session.merge(model)
        with self.Session() as session:
            if isinstance(model,model.__class__):
                model_by_id = session.query(model.__class__).filter(model.__class__.id == model.id)
                session.merge(model)
            else:
                raise TypeError("Argument must be an instance of the model class")
            session.commit()
    def update_old_id_in_model(self,model,id):
        with self.Session() as session:
            if isinstance(model, model.__class__):
                session.query(model.__class__).filter(model.__class__.id == model.id).update(
                    {model.__class__.old_id: id}, synchronize_session=False)
            else:
                raise TypeError("Argument must be an instance of the model class")
            session.commit()



class RedisConnection:
    def __init__(self, host, port, db):
        self.session = redis.Redis(host=host, port=port, db=db)

    def get_by_key(self,key):
        return self.session.get(key)

    def add(self,key,value):
        return self.session.set(key,value)

    def remove(self,key):
        return self.session.delete(key)
