 # <h1 align="center"><b>garrafa-unica</b><h1/><br>



 <p align="center" >Projeto de Business Intelligence desenvolvido para simular a operação de uma empresa de personalização e comercialização de garrafas, squeezes e produtos térmicos.<p/><br><br>



O sistema contempla geração de dados sintéticos, modelagem relacional em PostgreSQL, processos ETL e análises financeiras voltadas ao suporte à tomada de decisão.<br><br>



<b>Objetivos</b><br><br>



• Simular uma base de dados empresarial realista.<br>

• Consolidar informações de vendas, custos, despesas e investimentos.<br>

• Gerar indicadores financeiros e operacionais.<br>

• Servir como base para dashboards e análises de Business Intelligence.<br><br>



<b>Estrutura do Projeto</b><br><br>



garrafa-unica-bi/<br>

│<br>

├── config.py            # Configurações gerais e conexão<br>

├── database.py          # Utilitários de banco de dados<br>

├── init.sql             # Criação do schema PostgreSQL<br>

├── data_generator.py    # Geração de dados sintéticos<br>

├── etl.py               # Pipeline ETL<br>

├── analysis.py          # KPIs e análises financeiras<br>

├── requirements.txt     # Dependências do projeto<br>

│<br>

└── data/<br>

    └── raw/             # Arquivos CSV gerados<br><br>



<b>Modelo de Dados</b><br><br>



O banco foi estruturado para representar os principais processos da empresa:<br><br>



• Fornecedores (suppliers)<br>

• Produtos (products)<br>

• Máquinas de personalização (machines)<br>

• Clientes (customers)<br>

• Pedidos (orders)<br>

• Itens dos pedidos (order_items)<br>

• Despesas (expenses)<br>

• Investimentos (investments)<br><br>



Além das tabelas, o projeto conta com views específicas para análises financeiras e gerenciais.<br><br>



<b>Principais Funcionalidades</b><br><br>



<b>Geração de Dados</b><br><br>



O módulo <i>data_generator.py</i> cria dados sintéticos para o período entre janeiro de 2023 e maio de 2026, incluindo:<br><br>



• Clientes<br>

• Pedidos<br>

• Produtos<br>

• Custos<br>

• Despesas<br>

• Investimentos<br><br>



<b>ETL</b><br><br>



O pipeline ETL realiza:<br><br>



• Leitura dos arquivos CSV.<br>

• Tratamento e padronização dos dados.<br>

• Carga das informações no PostgreSQL.<br><br>



Execução:<br><br>



python etl.py<br><br>



<b>Análises</b><br><br>



O módulo <i>analysis.py</i> disponibiliza métricas como:<br><br>



• Receita total<br>

• Lucro bruto<br>

• Lucro líquido<br>

• Margem bruta<br>

• Margem líquida<br>

• Ticket médio<br>

• Evolução mensal<br>

• Rentabilidade por produto<br>

• Classificação ABC de produtos<br><br>



<b>Tecnologias Utilizadas</b><br><br>



• Python<br>

• PostgreSQL<br>

• Pandas<br>

• NumPy<br>

• SQLAlchemy<br>

• Faker<br>

• Dash<br>

• Plotly<br><br>



<b>Instalação</b><br><br>



Clone o projeto:<br><br>



git clone <repositorio><br>

cd garrafa-unica-bi<br><br>



Instale as dependências:<br><br>



pip install -r requirements.txt<br><br>



Configure as variáveis de ambiente:<br><br>



DB_HOST=localhost<br>

DB_PORT=5432<br>

DB_NAME=garrafa_unica<br>

DB_USER=postgres<br>

DB_PASSWORD=postgres<br><br>



Crie o banco de dados e execute o script:<br><br>



psql -U postgres -d garrafa_unica -f init.sql<br><br>



<b>Desenvolvimento</b><br><br>



Este projeto foi desenvolvido como estudo e demonstração prática dos conceitos de:<br><br>



• Engenharia de Dados<br>

• ETL<br>

• Business Intelligence<br>

• Análise Financeira<br>

• Modelagem Relacional<br><br>



Parte da implementação e aceleração do desenvolvimento contou com o apoio de ferramentas de Inteligência Artificial, utilizadas como assistência técnica para geração de código, validação e documentação.<br><br>



<b>Licença</b><br><br>



Projeto desenvolvido para fins educacionais e de demonstração.
