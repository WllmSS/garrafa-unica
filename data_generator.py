"""
data_generator.py
Gerador de dados sintéticos para Garrafa Única Ltda.
Período: Jan/2023 – Mai/2026  (~3,5 anos)
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import date, timedelta
from faker import Faker

fake = Faker("pt_BR")
random.seed(42)
np.random.seed(42)

# ──────────────────────────────────────────────
# Parâmetros configuráveis
# ──────────────────────────────────────────────
START_DATE      = date(2023, 1, 1)
END_DATE        = date(2026, 5, 31)
N_ORDERS        = 1200          # pedidos totais no período
N_CUSTOMERS     = 170
AVG_MARGIN      = 0.42          # margem bruta média desejada
MONTHLY_GROWTH  = 0.015         # crescimento mensal médio (~1,5%)
SEASONALITY     = 0.35          # intensidade da sazonalidade

# Meses com picos sazonais (índice 1=jan … 12=dez)
SEASONAL_BOOST = {
    6:  1.30,   # Dia dos namorados (junho BR)
    7:  1.10,   # inverno / formaturas
    10: 1.15,   # outubro rosa / eventos corporativos
    11: 1.20,   # black friday
    12: 1.55,   # natal / fim de ano
}

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(OUT_DIR, exist_ok=True)


# ──────────────────────────────────────────────
# 1. Fornecedores
# ──────────────────────────────────────────────
def gen_suppliers() -> pd.DataFrame:
    data = [
        {"id": 1, "name": "VidroMax Indústria Ltda.",   "city": "São Paulo",      "state": "SP", "contact": "comercial@vidromax.com.br",    "payment_terms": 30},
        {"id": 2, "name": "PlastiPack Embalagens S.A.", "city": "Campinas",       "state": "SP", "contact": "vendas@plastipack.com.br",      "payment_terms": 45},
        {"id": 3, "name": "AquaBottle Com. e Ind.",     "city": "Joinville",      "state": "SC", "contact": "contato@aquabottle.com.br",     "payment_terms": 30},
        {"id": 4, "name": "ThermoFlask Distribuidora",  "city": "Porto Alegre",   "state": "RS", "contact": "thermoflask@email.com.br",      "payment_terms": 60},
        {"id": 5, "name": "Inova Squeeze Ltda.",        "city": "Belo Horizonte", "state": "MG", "contact": "vendas@inovasqueeze.com.br",    "payment_terms": 30},
        {"id": 6, "name": "EcoGlass Brasil",            "city": "Curitiba",       "state": "PR", "contact": "eco@ecoglass.com.br",           "payment_terms": 45},
    ]
    df = pd.DataFrame(data)
    df["created_at"] = START_DATE
    return df


# ──────────────────────────────────────────────
# 2. Produtos
# ──────────────────────────────────────────────
def gen_products() -> pd.DataFrame:
    products = [
        # (name, category, volume_ml, base_cost, supplier_id)
        ("Garrafa Plástica 350ml",      "plástico",  350,  4.50, 2),
        ("Garrafa Plástica 500ml",      "plástico",  500,  5.20, 2),
        ("Garrafa Plástica 750ml",      "plástico",  750,  6.80, 2),
        ("Squeeze Esportivo 500ml",     "squeeze",   500,  7.50, 5),
        ("Squeeze Premium 700ml",       "squeeze",   700,  9.00, 5),
        ("Garrafa Vidro 300ml",         "vidro",     300,  8.50, 1),
        ("Garrafa Vidro 500ml",         "vidro",     500, 10.80, 1),
        ("Garrafa Vidro 750ml",         "vidro",     750, 13.50, 6),
        ("Térmica Inox 350ml",          "térmica",   350, 18.00, 4),
        ("Térmica Inox 500ml",          "térmica",   500, 22.00, 4),
        ("Térmica Premium 1L",          "térmica",  1000, 32.00, 4),
        ("Canteen Alumínio 600ml",      "alumínio",  600, 15.00, 3),
        ("Garrafa Infusora 500ml",      "vidro",     500, 14.00, 1),
        ("Squeeze Kids 300ml",          "squeeze",   300,  6.00, 5),
        ("Garrafa Eco Biodegradável 500ml", "eco",   500,  9.50, 3),
        ("Caçamba Acrílica 1L",         "acrílico", 1000, 11.00, 2),
        ("Garrafa Personalizada Deluxe","plástico",  600,  8.00, 2),
        ("Copa Plástica 200ml",         "plástico",  200,  2.80, 2),
    ]
    rows = []
    for i, (name, cat, vol, cost, sup) in enumerate(products, start=1):
        rows.append({
            "id": i, "name": name, "category": cat, "volume_ml": vol,
            "base_cost": cost, "supplier_id": sup, "active": True,
            "created_at": START_DATE,
        })
    return pd.DataFrame(rows)


# ──────────────────────────────────────────────
# 3. Máquinas
# ──────────────────────────────────────────────
def gen_machines() -> pd.DataFrame:
    data = [
        {"id": 1, "name": "Sublimadora Pro XL",      "type": "sublimação",
         "investment_value": 28000, "acquisition_date": date(2023, 1, 15),
         "useful_life_years": 7, "energy_cost_per_hour": 3.50,
         "capacity_units_per_hour": 30, "maintenance_monthly": 350, "active": True},
        {"id": 2, "name": "Serigráfica Automática",  "type": "serigrafia",
         "investment_value": 45000, "acquisition_date": date(2023, 3, 10),
         "useful_life_years": 8, "energy_cost_per_hour": 5.20,
         "capacity_units_per_hour": 60, "maintenance_monthly": 600, "active": True},
        {"id": 3, "name": "Laser Fiber 30W",         "type": "laser",
         "investment_value": 18500, "acquisition_date": date(2023, 7, 22),
         "useful_life_years": 6, "energy_cost_per_hour": 2.80,
         "capacity_units_per_hour": 25, "maintenance_monthly": 280, "active": True},
        {"id": 4, "name": "UV Printer 6-cores",      "type": "UV",
         "investment_value": 85000, "acquisition_date": date(2024, 2, 5),
         "useful_life_years": 8, "energy_cost_per_hour": 7.80,
         "capacity_units_per_hour": 80, "maintenance_monthly": 950, "active": True},
    ]
    return pd.DataFrame(data)


# ──────────────────────────────────────────────
# 4. Clientes
# ──────────────────────────────────────────────
def gen_customers(n: int = N_CUSTOMERS) -> pd.DataFrame:
    types    = ["PF", "PF", "PJ", "PJ", "Evento", "Revendedor"]
    segments = {
        "PF":        ["varejo"],
        "PJ":        ["corporativo", "varejo"],
        "Evento":    ["eventos"],
        "Revendedor":["varejo", "corporativo"],
    }
    states = ["SP","SP","SP","RJ","RS","MG","SC","PR","BA","GO"]
    rows = []
    for i in range(1, n + 1):
        t   = random.choice(types)
        seg = random.choice(segments[t])
        rows.append({
            "id": i,
            "name": fake.company() if t in ("PJ","Revendedor") else fake.name(),
            "type": t,
            "email": fake.email(),
            "city":  fake.city(),
            "state": random.choice(states),
            "segment": seg,
            "created_at": fake.date_between(START_DATE, date(2024, 6, 1)),
        })
    return pd.DataFrame(rows)


# ──────────────────────────────────────────────
# 5. Pedidos + Itens
# ──────────────────────────────────────────────
def _date_weights(start: date, end: date) -> tuple[list[date], list[float]]:
    """Gera lista de datas com pesos sazonais + tendência de crescimento."""
    dates, weights = [], []
    cur = start
    month_idx = 0
    while cur <= end:
        month = cur.month
        base_weight = 1.0 + MONTHLY_GROWTH * month_idx
        seasonal = SEASONAL_BOOST.get(month, 1.0)
        w = base_weight * (1 + (seasonal - 1) * SEASONALITY)
        dates.append(cur)
        weights.append(w)
        cur += timedelta(days=1)
        if cur.month != (cur - timedelta(days=1)).month:
            month_idx += 1
    total = sum(weights)
    return dates, [w / total for w in weights]


def gen_orders_and_items(
    customers: pd.DataFrame,
    products: pd.DataFrame,
    machines: pd.DataFrame,
    n_orders: int = N_ORDERS,
) -> tuple[pd.DataFrame, pd.DataFrame]:

    dates, weights = _date_weights(START_DATE, END_DATE)

    pay_methods  = ["PIX","PIX","Boleto","Cartão de Crédito","Cartão de Débito","Transferência"]
    machine_pool = machines["id"].tolist()
    prod_pool    = products["id"].tolist()
    cust_pool    = customers["id"].tolist()

    # pesos por tipo de cliente (PJ e Revendedor compram mais)
    cust_weights = customers.apply(
        lambda r: 3.0 if r["type"] in ("PJ","Revendedor") else 1.5 if r["type"] == "Evento" else 1.0,
        axis=1
    ).values
    cust_weights = cust_weights / cust_weights.sum()

    order_rows, item_rows = [], []
    order_id = item_id = 1

    for _ in range(n_orders):
        o_date    = random.choices(dates, weights=weights, k=1)[0]
        cust_id   = random.choices(cust_pool, weights=cust_weights, k=1)[0]
        pay       = random.choice(pay_methods)
        n_items   = random.choices([1,2,3,4,5], weights=[35,30,18,10,7], k=1)[0]
        delivery  = o_date + timedelta(days=random.randint(3, 15))

        total_rev = total_cost = 0.0
        for _ in range(n_items):
            prod_id  = random.choice(prod_pool)
            mach_id  = random.choice(machine_pool)
            prod_row = products[products["id"] == prod_id].iloc[0]
            mach_row = machines[machines["id"] == mach_id].iloc[0]
            qty      = random.choices(
                [10, 25, 50, 100, 200, 500],
                weights=[25, 30, 20, 15, 7, 3], k=1
            )[0]

            base_cost = float(prod_row["base_cost"])

            # custo personalização: energia + tinta + depreciação + mão de obra
            hours_per_batch   = qty / mach_row["capacity_units_per_hour"]
            energy_cost_unit  = mach_row["energy_cost_per_hour"] * hours_per_batch / qty
            ink_cost_unit     = random.uniform(0.40, 1.80)
            depr_monthly      = mach_row["investment_value"] / (mach_row["useful_life_years"] * 12)
            depr_unit         = depr_monthly / (mach_row["capacity_units_per_hour"] * 160)  # 160h/mês
            labor_unit        = random.uniform(0.80, 2.50)
            person_cost       = round(energy_cost_unit + ink_cost_unit + depr_unit + labor_unit, 4)

            total_unit_cost   = base_cost + person_cost

            # preço de venda com margem alvo ± variação
            margin_factor = AVG_MARGIN + random.gauss(0, 0.06)
            margin_factor = max(0.18, min(0.72, margin_factor))
            unit_price    = round(total_unit_cost / (1 - margin_factor), 2)

            item_rows.append({
                "id":                       item_id,
                "order_id":                 order_id,
                "product_id":               prod_id,
                "machine_id":               mach_id,
                "quantity":                 qty,
                "unit_price":               unit_price,
                "unit_base_cost":           round(base_cost, 4),
                "unit_personalization_cost":round(person_cost, 4),
            })
            total_rev  += qty * unit_price
            total_cost += qty * total_unit_cost
            item_id += 1

        order_rows.append({
            "id":            order_id,
            "customer_id":   cust_id,
            "order_date":    o_date,
            "delivery_date": delivery,
            "status":        "concluido",
            "payment_method":pay,
            "total_revenue": round(total_rev, 2),
            "total_cost":    round(total_cost, 2),
        })
        order_id += 1

    return pd.DataFrame(order_rows), pd.DataFrame(item_rows)


# ──────────────────────────────────────────────
# 6. Despesas mensais
# ──────────────────────────────────────────────
def gen_expenses(orders: pd.DataFrame) -> pd.DataFrame:
    rows = []
    exp_id = 1
    cur = START_DATE.replace(day=1)
    end = END_DATE.replace(day=1)

    while cur <= end:
        month_rev = orders[
            (orders["order_date"] >= cur) &
            (orders["order_date"] < (cur.replace(month=cur.month % 12 + 1) if cur.month < 12
                                     else cur.replace(year=cur.year + 1, month=1)))
        ]["total_revenue"].sum()

        # FIXAS
        fixed_items = [
            ("Aluguel",          "aluguel",    "fixo",    3800),
            ("Salários",         "salários",   "fixo",    12000 + cur.month % 3 * 400),
            ("Pró-labore",       "salários",   "fixo",    4500),
            ("Internet/Telefone","infra",       "fixo",    350),
            ("Contabilidade",    "serviços",    "fixo",    800),
            ("Software/ERP",     "TI",          "fixo",    290),
        ]
        for desc, cat, tp, val in fixed_items:
            rows.append({
                "id": exp_id, "expense_date": cur.replace(day=5),
                "category": cat, "type": tp, "description": desc,
                "amount": val + random.gauss(0, val * 0.02),
                "payment_status": "pago",
            })
            exp_id += 1

        # VARIÁVEIS (proporcionais à receita)
        var_items = [
            ("Tinta e insumos",   "insumos",    "variável", 0.04),
            ("Energia elétrica",  "energia",    "variável", 0.025),
            ("Embalagem/Entrega", "logística",  "variável", 0.03),
            ("Marketing Digital", "marketing",  "variável", 0.02),
            ("Comissão Vendedores","comissões",  "variável", 0.015),
        ]
        for desc, cat, tp, pct in var_items:
            val = month_rev * pct if month_rev > 0 else 800
            rows.append({
                "id": exp_id, "expense_date": cur.replace(day=15),
                "category": cat, "type": tp, "description": desc,
                "amount": round(val + random.gauss(0, val * 0.05), 2),
                "payment_status": "pago",
            })
            exp_id += 1

        # Manutenção de máquinas
        rows.append({
            "id": exp_id, "expense_date": cur.replace(day=20),
            "category": "manutenção", "type": "fixo",
            "description": "Manutenção preventiva máquinas",
            "amount": round(2180 + random.gauss(0, 150), 2),
            "payment_status": "pago",
        })
        exp_id += 1

        # Avança mês
        if cur.month == 12:
            cur = cur.replace(year=cur.year + 1, month=1)
        else:
            cur = cur.replace(month=cur.month + 1)

    return pd.DataFrame(rows)


# ──────────────────────────────────────────────
# 7. Investimentos
# ──────────────────────────────────────────────
def gen_investments(machines: pd.DataFrame) -> pd.DataFrame:
    data = [
        # máquinas
        {"id":1, "investment_date": date(2023,1,10), "category":"máquina",
         "description":"Sublimadora Pro XL - aquisição",
         "amount":28000, "expected_return_months":18, "machine_id":1, "notes":"Financiado 50%"},
        {"id":2, "investment_date": date(2023,3,5),  "category":"máquina",
         "description":"Serigráfica Automática - aquisição",
         "amount":45000, "expected_return_months":24, "machine_id":2, "notes":"À vista"},
        {"id":3, "investment_date": date(2023,7,18), "category":"máquina",
         "description":"Laser Fiber 30W - aquisição",
         "amount":18500, "expected_return_months":12, "machine_id":3, "notes":"Leasing 24x"},
        {"id":4, "investment_date": date(2024,2,1),  "category":"máquina",
         "description":"UV Printer 6-cores - aquisição",
         "amount":85000, "expected_return_months":30, "machine_id":4, "notes":"Financiado BNDES"},
        # outros
        {"id":5, "investment_date": date(2023,2,1),  "category":"reforma",
         "description":"Reforma e adequação do galpão",
         "amount":22000, "expected_return_months":36, "machine_id": None, "notes":"Obra civil"},
        {"id":6, "investment_date": date(2023,6,1),  "category":"marketing",
         "description":"Site + branding + Google Ads",
         "amount":8500,  "expected_return_months":12, "machine_id": None, "notes":"Agência parceira"},
        {"id":7, "investment_date": date(2024,1,1),  "category":"TI",
         "description":"Sistema ERP e BI - implantação",
         "amount":12000, "expected_return_months":18, "machine_id": None, "notes":"Licença anual + setup"},
        {"id":8, "investment_date": date(2025,1,1),  "category":"marketing",
         "description":"Campanha de Influencers 2025",
         "amount":15000, "expected_return_months":9,  "machine_id": None, "notes":"Instagram + YouTube"},
    ]
    return pd.DataFrame(data)


# ──────────────────────────────────────────────
# 8. Salvar CSVs
# ──────────────────────────────────────────────
def save_all(out_dir: str = OUT_DIR):
    print("🔄 Gerando dados...")
    suppliers  = gen_suppliers()
    products   = gen_products()
    machines   = gen_machines()
    customers  = gen_customers()
    orders, items = gen_orders_and_items(customers, products, machines)
    expenses   = gen_expenses(orders)
    investments= gen_investments(machines)

    dfs = {
        "suppliers":   suppliers,
        "products":    products,
        "machines":    machines,
        "customers":   customers,
        "orders":      orders,
        "order_items": items,
        "expenses":    expenses,
        "investments": investments,
    }
    for name, df in dfs.items():
        path = os.path.join(out_dir, f"{name}.csv")
        df.to_csv(path, index=False)
        print(f"  ✅ {name}.csv  →  {len(df):,} registros")

    print(f"\n📊 Resumo:")
    print(f"  Pedidos: {len(orders):,}  |  Itens: {len(items):,}")
    print(f"  Receita total: R$ {orders['total_revenue'].sum():,.2f}")
    print(f"  Margem bruta média: {((orders['total_revenue'].sum() - orders['total_cost'].sum()) / orders['total_revenue'].sum() * 100):.1f}%")
    return dfs


if __name__ == "__main__":
    save_all()