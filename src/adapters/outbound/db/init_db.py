from sqlalchemy import text
from src.adapters.outbound.db.session import engine

def verify_db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("Database connected successfully")
    except Exception as e:
        print("Database connection failed")
        print(e)