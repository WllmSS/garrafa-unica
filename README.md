# garrafa-unica


Projeto de Business Intelligence desenvolvido para simular a operação de uma empresa de personalização e comercialização de garrafas, squeezes e produtos térmicos.

O sistema contempla geração de dados sintéticos, modelagem relacional em PostgreSQL, processos ETL e análises financeiras para suporte à tomada de decisão.

Objetivos
Simular uma base de dados empresarial realista.
Consolidar informações de vendas, custos, despesas e investimentos.
Gerar indicadores financeiros e operacionais.
Servir como base para dashboards e análises de BI.
Estrutura do Projeto
garrafa-unica-bi/
│
├── config.py            # Configurações gerais e conexão
├── database.py          # Utilitários de banco de dados
├── init.sql             # Criação do schema PostgreSQL
├── data_generator.py    # Geração de dados sintéticos
├── etl.py               # Pipeline ETL
├── analysis.py          # KPIs e análises financeiras
├── requirements.txt     # Dependências do projeto
│
└── data/
    └── raw/             # Arquivos CSV gerados
Modelo de Dados

O banco foi estruturado para representar os principais processos da empresa:

Fornecedores (suppliers)
Produtos (products)
Máquinas de personalização (machines)
Clientes (customers)
Pedidos (orders)
Itens dos pedidos (order_items)
Despesas (expenses)
Investimentos (investments)

Além das tabelas, o projeto possui views voltadas para análises financeiras e gerenciais.

Principais Funcionalidades
Geração de Dados

O módulo data_generator.py cria dados sintéticos entre janeiro de 2023 e maio de 2026, incluindo:

Clientes
Pedidos
Produtos
Custos
Despesas
Investimentos
ETL

O pipeline ETL realiza:

Leitura dos arquivos CSV.
Tratamento e padronização dos dados.
Carga das informações no PostgreSQL.

Execução:

python etl.py
Análises

O módulo analysis.py disponibiliza métricas como:

Receita total
Lucro bruto
Lucro líquido
Margem bruta
Margem líquida
Ticket médio
Evolução mensal
Rentabilidade por produto
Classificação ABC de produtos
Tecnologias Utilizadas
Python
PostgreSQL
Pandas
NumPy
SQLAlchemy
Faker
Dash
Plotly
Instalação

Clone o projeto:

git clone <repositorio>
cd garrafa-unica-bi

Instale as dependências:

pip install -r requirements.txt

Configure as variáveis de ambiente:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=garrafa_unica
DB_USER=postgres
DB_PASSWORD=postgres

Crie o banco de dados e execute o script:

psql -U postgres -d garrafa_unica -f init.sql
Desenvolvimento

Este projeto foi desenvolvido como estudo e demonstração de conceitos de:

Engenharia de Dados
ETL
Business Intelligence
Análise Financeira
Modelagem Relacional

Parte da implementação e aceleração do desenvolvimento contou com o apoio de ferramentas de Inteligência Artificial, utilizadas como assistência técnica para geração de código, validação e documentação.

Licença

Projeto desenvolvido para fins educacionais e de demonstração.
