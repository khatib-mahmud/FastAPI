from abc import ABC

import sqlalchemy
from sqlalchemy import create_engine, func, asc, desc
from sqlalchemy.orm import sessionmaker
from Repository.IRepositoryBase import IRepositoryBase


class RepositoryBase(IRepositoryBase, ABC):
    def __init__(self, entity: type) -> None:
        # self.engine = create_engine('sqlite:///:database:', echo=False)

        self.engine = create_engine('mysql+mysqlconnector://root:123456@10.11.201.40/credit_score_db', echo=False)
        # self.engine = create_engine('mysql+mysqlconnector://root:root#1234@localhost/credit_scoring', echo=False)

        session_maker = sessionmaker(bind=self.engine)
        self.session = session_maker()
        self.entity_type = entity

        # Check if table exists
        inspector = sqlalchemy.engine.reflection.Inspector(self.engine)
        if inspector.has_table(entity.__tablename__) is False:
            entity.__table__.create(self.engine)

    def get_version(self):
        return sqlalchemy.__version__

    def add(self, data) -> None:
        self.session.add(data)
        self.session.commit()

    def delete(self, data) -> None:
        self.session.delete(data)
        self.session.commit()

    def commit(self) -> None:
        self.session.commit()

    def get_all(self) -> list:
        return self.session.query(self.entity_type).all()

    def get_count(self) -> int:
        return self.session.query(self.entity_type).count()

    def get(self, *args) -> list:
        return self.session.query(self.entity_type).filter(*args).all()

    def order_by_desc(self, col_map, *args) -> list:
        return self.session.query(self.entity_type).filter(*args).order_by(desc(col_map))

    def order_by_asc(self, col_map, *args) -> list:
        return self.session.query(self.entity_type).filter(*args).order_by(asc(col_map))

    def get_col(self, *args) -> list:
        return self.session.query(*args).all()

    def max(self, col_map) -> int:
        return self.session.query(func.max(col_map)).scalar()

    def close(self):
        self.session.close()

    def __del__(self):
        self.session.close()