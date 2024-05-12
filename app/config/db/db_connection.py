from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis


class MysqlConnection:
    def __init__(self, host, port, user, password, base):
        self.engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{base}')
        self.Session = sessionmaker(bind=self.engine)

    def close(self):
        self.engine.dispose()

    def get_row_by_table_and_id(self, id, model):
        with self.Session() as session:
            return session.get(model, id)

    def get_trigger_row_by_rec_id(self,rec_id,model):
        with self.Session() as session:
            return session.query(model).filter(model.record_id == rec_id).first()
    def get_by_table_and_no_sync(self, model,table_name) -> []:
        with self.Session() as session:
            return session.query(model).filter(model.is_synced == False).filter(model.table_name == table_name).all()

    def create_record(self, model_instance):
        with self.Session() as session:
            session.add(model_instance)
            session.commit()

            # Если используете SQLite или другую базу данных, которая не возвращает сгенерированный ID автоматически
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


class RedisConnection:
    def __init__(self, host, port, db):
        self.session = redis.Redis(host=host, port=port, db=db)

    def get_by_key(self,key):
        return self.session.get(key)

    def add(self,key,value):
        return self.session.set(key,value)

    def remove(self,key):
        return self.session.delete(key)
