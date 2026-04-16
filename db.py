from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:postgres123@127.0.0.1:5434/health_db"
)