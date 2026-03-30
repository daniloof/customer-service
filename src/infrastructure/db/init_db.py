from sqlalchemy import text
from src.infrastructure.db.session import engine

def test_db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("Database connected successfuly")
    except Exception as e:
        print("Database connection failed")
        print(e)