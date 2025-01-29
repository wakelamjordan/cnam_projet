from app.database import db_session
from sqlalchemy import text
class Manager:
    @staticmethod
    def query_sql(sql: str, params: list = []):

        return db_session.execute(text(sql), params)