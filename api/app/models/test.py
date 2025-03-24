from sqlalchemy import Column, Integer, String
from app.database import Base


class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, autoincrement=True, primary_key=True)
    nom = Column(String(50))

    def __init__(self, nom):
        self.nom = nom

    def __repr__(self):
        return f"<(id='{self.id}', nom='{self.nom}')>"
        # return {'id': self.id, 'nom': self.nom}
