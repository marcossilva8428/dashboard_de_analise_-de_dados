# dashboard_de_analise_-de_dados
Aplicação web que mostra visualizações de dados usando Python (Flask/Django), SQL e bibliotecas como Pandas, Matplotlib ou Plotly


dashboard_app/
├── app.py                  # Arquivo principal Flask
├── config.py               # Configurações (DB, etc)
├── requirements.txt        # Dependências
├── database/
│   ├── schema.sql          # Estrutura do banco de dados
│   └── seed_data.sql       # Dados de exemplo
├── static/
│   ├── css/                # Estilos CSS
│   └── js/                 # Scripts JavaScript
├── templates/              # Templates HTML
│   ├── base.html           # Template base
│   ├── index.html          # Página principal
│   └── dashboard.html      # Dashboard principal
└── utils/
    └── db_operations.py    # Funções de banco de dados
