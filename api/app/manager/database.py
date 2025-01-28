from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
# from flask import current_app

# engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
# je ne parviens pas à déplacer ce paramétre dans config c'est bien dommage
engine = create_engine('sqlite:///cnam_projet.db')
# engine = create_engine('mysql+pymysql://root:4321@localhost:3306/cnam_projet')

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import app.models.user
    Base.metadata.create_all(bind=engine)
