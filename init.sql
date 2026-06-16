-- ============================================================
-- Schema PostgreSQL - Garrafa Única Ltda. BI
-- ============================================================

CREATE TABLE IF NOT EXISTS suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(80),
    state VARCHAR(2),
    contact VARCHAR(100),
    payment_terms INTEGER DEFAULT 30,  -- dias
    created_at DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),          -- ex: térmica, squeeze, vidro, plástico
    volume_ml INTEGER,
    base_cost NUMERIC(10,2),       -- custo de compra em branco
    supplier_id INTEGER REFERENCES suppliers(id),
    active BOOLEAN DEFAULT TRUE,
    created_at DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS machines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(60),              -- sublimação, serigrafia, laser, UV
    investment_value NUMERIC(12,2),
    acquisition_date DATE,
    useful_life_years INTEGER DEFAULT 5,
    energy_cost_per_hour NUMERIC(8,2),
    capacity_units_per_hour INTEGER,
    maintenance_monthly NUMERIC(10,2),
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    type VARCHAR(30),              -- PF, PJ, Evento, Revendedor
    email VARCHAR(120),
    city VARCHAR(80),
    state VARCHAR(2),
    segment VARCHAR(50),           -- corporativo, varejo, eventos
    created_at DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    order_date DATE NOT NULL,
    delivery_date DATE,
    status VARCHAR(30) DEFAULT 'concluido',
    payment_method VARCHAR(40),
    total_revenue NUMERIC(12,2),
    total_cost NUMERIC(12,2),
    gross_profit NUMERIC(12,2) GENERATED ALWAYS AS (total_revenue - total_cost) STORED,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    machine_id INTEGER REFERENCES machines(id),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10,2),      -- preço de venda por unidade
    unit_base_cost NUMERIC(10,2),  -- custo garrafa em branco
    unit_personalization_cost NUMERIC(10,2),  -- custo personalização
    unit_total_cost NUMERIC(10,2) GENERATED ALWAYS AS (unit_base_cost + unit_personalization_cost) STORED,
    line_revenue NUMERIC(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    line_cost NUMERIC(12,2) GENERATED ALWAYS AS (quantity * (unit_base_cost + unit_personalization_cost)) STORED
);

CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    expense_date DATE NOT NULL,
    category VARCHAR(60),          -- aluguel, salários, energia, tinta, manutenção, mkt
    type VARCHAR(20),              -- fixo, variável
    description VARCHAR(200),
    amount NUMERIC(12,2),
    payment_status VARCHAR(20) DEFAULT 'pago'
);

CREATE TABLE IF NOT EXISTS investments (
    id SERIAL PRIMARY KEY,
    investment_date DATE NOT NULL,
    category VARCHAR(60),          -- máquina, reforma, marketing, TI
    description VARCHAR(200),
    amount NUMERIC(12,2),
    expected_return_months INTEGER,
    machine_id INTEGER REFERENCES machines(id),
    notes TEXT
);

-- ============================================================
-- VIEWS financeiras
-- ============================================================

CREATE OR REPLACE VIEW financial_monthly AS
SELECT
    DATE_TRUNC('month', o.order_date) AS month,
    COUNT(DISTINCT o.id)              AS total_orders,
    SUM(o.total_revenue)              AS revenue,
    SUM(o.total_cost)                 AS cogs,
    SUM(o.gross_profit)               AS gross_profit,
    ROUND(SUM(o.gross_profit) / NULLIF(SUM(o.total_revenue),0) * 100, 2) AS gross_margin_pct
FROM orders o
WHERE o.status = 'concluido'
GROUP BY 1
ORDER BY 1;

CREATE OR REPLACE VIEW product_profitability AS
SELECT
    p.id,
    p.name,
    p.category,
    SUM(oi.quantity)                  AS units_sold,
    SUM(oi.line_revenue)              AS total_revenue,
    SUM(oi.line_cost)                 AS total_cost,
    SUM(oi.line_revenue - oi.line_cost) AS gross_profit,
    ROUND(SUM(oi.line_revenue - oi.line_cost) / NULLIF(SUM(oi.line_revenue),0) * 100, 2) AS margin_pct
FROM order_items oi
JOIN products p ON p.id = oi.product_id
JOIN orders o ON o.id = oi.order_id
WHERE o.status = 'concluido'
GROUP BY p.id, p.name, p.category
ORDER BY gross_profit DESC;

CREATE OR REPLACE VIEW customer_profitability AS
SELECT
    c.id,
    c.name,
    c.type,
    c.segment,
    COUNT(DISTINCT o.id)              AS total_orders,
    SUM(o.total_revenue)              AS lifetime_revenue,
    SUM(o.total_cost)                 AS lifetime_cost,
    SUM(o.gross_profit)               AS lifetime_profit,
    ROUND(SUM(o.gross_profit) / NULLIF(SUM(o.total_revenue),0) * 100, 2) AS margin_pct,
    MIN(o.order_date)                 AS first_order,
    MAX(o.order_date)                 AS last_order
FROM customers c
JOIN orders o ON o.customer_id = c.id
WHERE o.status = 'concluido'
GROUP BY c.id, c.name, c.type, c.segment
ORDER BY lifetime_profit DESC;

CREATE OR REPLACE VIEW machine_roi AS
SELECT
    m.id,
    m.name,
    m.type,
    m.investment_value,
    m.acquisition_date,
    COALESCE(SUM(oi.line_revenue - oi.line_cost), 0) AS total_contribution,
    ROUND(COALESCE(SUM(oi.line_revenue - oi.line_cost), 0) / NULLIF(m.investment_value,0) * 100, 2) AS roi_pct,
    CASE
        WHEN COALESCE(SUM(oi.line_revenue - oi.line_cost),0) > 0
        THEN ROUND(m.investment_value / (SUM(oi.line_revenue - oi.line_cost) / 12.0), 1)
        ELSE NULL
    END AS payback_months
FROM machines m
LEFT JOIN order_items oi ON oi.machine_id = m.id
LEFT JOIN orders o ON o.id = oi.order_id AND o.status = 'concluido'
GROUP BY m.id, m.name, m.type, m.investment_value, m.acquisition_date;