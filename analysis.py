"""
analysis.py  –  Cálculos financeiros avançados (sem banco: usa DataFrames)
Pode ser usado tanto pelo ETL quanto diretamente pelo dashboard.
"""
import pandas as pd
import numpy as np


# ──────────────────────────────────────────────
# Helpers de carregamento (CSV ou DB)
# ──────────────────────────────────────────────
def load_from_csv(data_dir: str) -> dict[str, pd.DataFrame]:
    import os
    tables = ["suppliers","products","machines","customers",
              "orders","order_items","expenses","investments"]
    dfs = {}
    for t in tables:
        path = os.path.join(data_dir, f"{t}.csv")
        if os.path.exists(path):
            dfs[t] = pd.read_csv(path, parse_dates=["order_date","expense_date",
                                                      "investment_date","created_at",
                                                      "acquisition_date",
                                                      "delivery_date"], errors="ignore")
    return dfs


# ──────────────────────────────────────────────
# 1. KPIs gerais
# ──────────────────────────────────────────────
def kpis(orders: pd.DataFrame, expenses: pd.DataFrame) -> dict:
    rev   = orders["total_revenue"].sum()
    cogs  = orders["total_cost"].sum()
    gp    = rev - cogs
    total_exp = expenses["amount"].sum()
    net   = gp - total_exp

    return {
        "receita_total":    rev,
        "custo_mercadoria": cogs,
        "lucro_bruto":      gp,
        "margem_bruta_pct": gp / rev * 100 if rev else 0,
        "despesas_totais":  total_exp,
        "lucro_liquido":    net,
        "margem_liquida_pct": net / rev * 100 if rev else 0,
        "total_pedidos":    len(orders),
        "ticket_medio":     rev / len(orders) if len(orders) else 0,
    }


# ──────────────────────────────────────────────
# 2. Evolução mensal
# ──────────────────────────────────────────────
def monthly_evolution(orders: pd.DataFrame, expenses: pd.DataFrame) -> pd.DataFrame:
    orders = orders.copy()
    orders["month"] = pd.to_datetime(orders["order_date"]).dt.to_period("M").dt.to_timestamp()

    rev_df = (
        orders.groupby("month")
        .agg(receita=("total_revenue","sum"),
             custo_mercadoria=("total_cost","sum"),
             pedidos=("id","count"))
        .reset_index()
    )
    rev_df["lucro_bruto"]     = rev_df["receita"] - rev_df["custo_mercadoria"]
    rev_df["margem_bruta_pct"]= rev_df["lucro_bruto"] / rev_df["receita"] * 100

    expenses = expenses.copy()
    expenses["month"] = pd.to_datetime(expenses["expense_date"]).dt.to_period("M").dt.to_timestamp()
    exp_df = expenses.groupby("month")["amount"].sum().reset_index(name="despesas")

    df = rev_df.merge(exp_df, on="month", how="left").fillna(0)
    df["lucro_liquido"]     = df["lucro_bruto"] - df["despesas"]
    df["margem_liquida_pct"]= df["lucro_liquido"] / df["receita"] * 100
    return df.sort_values("month")


# ──────────────────────────────────────────────
# 3. Rentabilidade por produto
# ──────────────────────────────────────────────
def product_profitability(order_items: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    oi = order_items.copy()
    oi["line_revenue"] = oi["quantity"] * oi["unit_price"]
    oi["line_cost"]    = oi["quantity"] * (oi["unit_base_cost"] + oi["unit_personalization_cost"])
    oi["line_profit"]  = oi["line_revenue"] - oi["line_cost"]

    df = (
        oi.groupby("product_id")
        .agg(
            unidades=("quantity","sum"),
            receita=("line_revenue","sum"),
            custo=("line_cost","sum"),
            lucro=("line_profit","sum"),
        )
        .reset_index()
        .rename(columns={"product_id":"id"})
    )
    df["margem_pct"] = df["lucro"] / df["receita"] * 100
    df = df.merge(products[["id","name","category"]], on="id", how="left")

    # ABC: top 20% receita = A, próx 30% = B, resto = C
    df = df.sort_values("receita", ascending=False)
    df["receita_cum_pct"] = df["receita"].cumsum() / df["receita"].sum() * 100
    df["abc"] = df["receita_cum_pct"].apply(
        lambda x: "A" if x <= 60 else ("B" if x <= 85 else "C")
    )
    return df


# ──────────────────────────────────────────────
# 4. Rentabilidade por cliente + RFM + LTV
# ──────────────────────────────────────────────
def customer_analysis(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    o = orders.copy()
    o["order_date"] = pd.to_datetime(o["order_date"])
    snapshot = o["order_date"].max()

    rfm = (
        o.groupby("customer_id")
        .agg(
            recency=("order_date",  lambda x: (snapshot - x.max()).days),
            frequency=("id",        "count"),
            monetary=("total_revenue","sum"),
            custo=("total_cost","sum"),
        )
        .reset_index()
        .rename(columns={"customer_id":"id"})
    )
    rfm["lucro"]      = rfm["monetary"] - rfm["custo"]
    rfm["margem_pct"] = rfm["lucro"] / rfm["monetary"] * 100
    rfm["ticket_medio"]= rfm["monetary"] / rfm["frequency"]

    # LTV simples: monetário médio mensal × 24 meses esperados
    rfm["ltv_estimado"] = rfm["ticket_medio"] * rfm["frequency"] / 3.5 * 24   # 3,5 anos de dados

    # Score RFM (1-5 cada dimensão)
    for col, asc in [("recency",True),("frequency",False),("monetary",False)]:
        label = col[0].upper()
        rfm[f"{label}_score"] = pd.qcut(rfm[col], 5, labels=[5,4,3,2,1] if asc else [1,2,3,4,5], duplicates="drop")
    rfm["rfm_score"] = (
        rfm["R_score"].astype(int) + rfm["F_score"].astype(int) + rfm["M_score"].astype(int)
    )
    rfm["segmento_rfm"] = rfm["rfm_score"].apply(
        lambda s: "Champions" if s >= 13 else
                  ("Loyal" if s >= 10 else
                  ("At Risk" if s >= 7 else "Lost"))
    )

    return rfm.merge(customers[["id","name","type","segment"]], on="id", how="left")


# ──────────────────────────────────────────────
# 5. ROI e Payback por máquina
# ──────────────────────────────────────────────
def machine_roi(order_items: pd.DataFrame, machines: pd.DataFrame) -> pd.DataFrame:
    oi = order_items.copy()
    oi["contribution"] = (
        oi["quantity"] * oi["unit_price"]
        - oi["quantity"] * (oi["unit_base_cost"] + oi["unit_personalization_cost"])
    )
    contrib = (
        oi.groupby("machine_id")["contribution"]
        .sum()
        .reset_index()
        .rename(columns={"machine_id":"id"})
    )
    df = machines.merge(contrib, on="id", how="left").fillna({"contribution": 0})

    df["roi_pct"]        = df["contribution"] / df["investment_value"] * 100
    df["depr_mensal"]    = df["investment_value"] / (df["useful_life_years"] * 12)

    # payback em meses (contribuição acumulada mensal média)
    total_months = (pd.Timestamp("2026-05-31") - pd.Timestamp("2023-01-01")).days / 30.44
    df["contrib_mensal"] = df["contribution"] / total_months
    df["payback_meses"]  = np.where(
        df["contrib_mensal"] > 0,
        df["investment_value"] / df["contrib_mensal"],
        np.nan
    )
    return df


# ──────────────────────────────────────────────
# 6. Break-even mensal
# ──────────────────────────────────────────────
def break_even(expenses: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    monthly = monthly_evolution(orders, expenses)
    fixed   = expenses[expenses["type"] == "fixo"].groupby(
        pd.to_datetime(expenses[expenses["type"] == "fixo"]["expense_date"]).dt.to_period("M").dt.to_timestamp()
    )["amount"].sum().reset_index(name="custos_fixos").rename(columns={"expense_date":"month"})

    df = monthly.merge(fixed, on="month", how="left").fillna(0)
    df["ponto_equilíbrio"] = df["custos_fixos"] / (df["margem_bruta_pct"] / 100).replace(0, np.nan)
    df["acima_be"] = df["receita"] >= df["ponto_equilíbrio"]
    return df[["month","receita","custos_fixos","ponto_equilíbrio","acima_be"]]


# ──────────────────────────────────────────────
# 7. Despesas por categoria
# ──────────────────────────────────────────────
def expenses_breakdown(expenses: pd.DataFrame) -> pd.DataFrame:
    return (
        expenses.groupby(["category","type"])["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )