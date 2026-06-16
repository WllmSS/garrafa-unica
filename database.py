import pandas as pd
from sqlalchemy import create_engine, text
from config import DATABASE_URL


def get_engine():
    return create_engine(DATABASE_URL, pool_pre_ping=True)


def query(sql: str, params: dict | None = None) -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params)


def execute(sql: str, params: dict | None = None):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(sql), params or {})


def init_schema(sql_path: str):
    with open(sql_path, "r", encoding="utf-8") as f:
        ddl = f.read()
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(ddl))
    print("✅ Schema criado com sucesso.")