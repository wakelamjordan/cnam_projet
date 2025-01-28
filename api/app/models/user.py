from sqlalchemy import Column, Integer, String, text
from app.manager.database import Base
from app.manager.database import db_session


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}

    # def to_dicts(datas):
    #     return [u.to_dict() for u in datas]

    def query_sql(sql: str, params: list = []):
        # return db_session.execute(sql)
        u = db_session.execute(text(sql), params)
        data = []
        for row in u:
            data.append({'id': row.id, 'name': row.name, 'email': row.email})
        return data

    # def __repr__(self):
    #     return f'<User id={self.id!r} name={self.name!r} email={self.email!r}>'
