"""
etl.py  –  Extract → Transform → Load para PostgreSQL
"""
import os
import pandas as pd
from sqlalchemy import text
from database import get_engine
from config import DATA_DIR


# ──────────────────────────────────────────────
# Extract
# ──────────────────────────────────────────────
def extract(table: str) -> pd.DataFrame:
    path = os.path.join(DATA_DIR, f"{table}.csv")
    df = pd.read_csv(path)
    print(f"  📥 {table}: {len(df):,} linhas lidas")
    return df


# ──────────────────────────────────────────────
# Transform
# ──────────────────────────────────────────────
def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    df["order_date"]    = pd.to_datetime(df["order_date"]).dt.date
    df["delivery_date"] = pd.to_datetime(df["delivery_date"]).dt.date
    df["total_revenue"] = df["total_revenue"].round(2)
    df["total_cost"]    = df["total_cost"].round(2)
    # remove coluna gerada (computed column no PG)
    df = df.drop(columns=["gross_profit"], errors="ignore")
    return df


def transform_order_items(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["unit_price","unit_base_cost","unit_personalization_cost"]:
        df[col] = df[col].round(4)
    # remove colunas geradas pelo PG
    for col in ["unit_total_cost","line_revenue","line_cost"]:
        df = df.drop(columns=[col], errors="ignore")
    return df


def transform_expenses(df: pd.DataFrame) -> pd.DataFrame:
    df["expense_date"] = pd.to_datetime(df["expense_date"]).dt.date
    df["amount"]       = df["amount"].round(2)
    return df


def transform_investments(df: pd.DataFrame) -> pd.DataFrame:
    df["investment_date"] = pd.to_datetime(df["investment_date"]).dt.date
    df["machine_id"]      = df["machine_id"].where(df["machine_id"].notna(), None)
    return df


def transform_machines(df: pd.DataFrame) -> pd.DataFrame:
    df["acquisition_date"] = pd.to_datetime(df["acquisition_date"]).dt.date
    return df


def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.date
    return df


TRANSFORMS = {
    "orders":       transform_orders,
    "order_items":  transform_order_items,
    "expenses":     transform_expenses,
    "investments":  transform_investments,
    "machines":     transform_machines,
    "customers":    transform_customers,
}


# ──────────────────────────────────────────────
# Load
# ──────────────────────────────────────────────
LOAD_ORDER = [
    "suppliers", "products", "machines", "customers",
    "orders", "order_items", "expenses", "investments",
]


def load(df: pd.DataFrame, table: str, engine):
    with engine.begin() as conn:
        conn.execute(text(f'TRUNCATE TABLE {table} RESTART IDENTITY CASCADE'))
        df.to_sql(table, conn, if_exists="append", index=False, method="multi", chunksize=500)
    print(f"  💾 {table}: {len(df):,} registros carregados")


# ──────────────────────────────────────────────
# Pipeline principal
# ──────────────────────────────────────────────
def run_etl():
    print("🚀 Iniciando ETL Garrafa Única...\n")
    engine = get_engine()

    for table in LOAD_ORDER:
        print(f"▶  {table}")
        df = extract(table)
        if table in TRANSFORMS:
            df = TRANSFORMS[table](df)
        load(df, table, engine)
        print()

    print("✅ ETL concluído com sucesso!")


if __name__ == "__main__":
    run_etl()