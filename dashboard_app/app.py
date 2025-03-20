from flask import Flask, render_template, jsonify, request
import pandas as pd
import json
import plotly
import plotly.express as px
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configuração do banco de dados
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///database/sales_data.db")
engine = create_engine(DATABASE_URI)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/sales_by_month')
def sales_by_month():
    query = """
    SELECT 
        strftime('%Y-%m', date) as month,
        SUM(amount) as total_sales
    FROM sales
    GROUP BY month
    ORDER BY month
    """
    
    with engine.connect() as connection:
        result = connection.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    # Criar gráfico com plotly
    fig = px.bar(df, x='month', y='total_sales', title='Vendas Mensais')
    
    # Converter para JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify(graphJSON)

@app.route('/api/sales_by_category')
def sales_by_category():
    query = """
    SELECT 
        category,
        SUM(amount) as total_sales
    FROM sales
    JOIN products ON sales.product_id = products.id
    GROUP BY category
    ORDER BY total_sales DESC
    """
    
    with engine.connect() as connection:
        result = connection.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    # Criar gráfico com plotly
    fig = px.pie(df, values='total_sales', names='category', title='Vendas por Categoria')
    
    # Converter para JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify(graphJSON)

@app.route('/api/sales_by_region')
def sales_by_region():
    query = """
    SELECT 
        region,
        SUM(amount) as total_sales
    FROM sales
    JOIN customers ON sales.customer_id = customers.id
    GROUP BY region
    ORDER BY total_sales DESC
    """
    
    with engine.connect() as connection:
        result = connection.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    # Criar gráfico com plotly
    fig = px.bar(df, x='region', y='total_sales', title='Vendas por Região')
    
    # Converter para JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify(graphJSON)

@app.route('/api/top_products')
def top_products():
    limit = request.args.get('limit', 10, type=int)
    
    query = f"""
    SELECT 
        products.name,
        SUM(amount) as total_sales
    FROM sales
    JOIN products ON sales.product_id = products.id
    GROUP BY products.name
    ORDER BY total_sales DESC
    LIMIT {limit}
    """
    
    with engine.connect() as connection:
        result = connection.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    # Criar gráfico com plotly
    fig = px.bar(df, x='name', y='total_sales', title=f'Top {limit} Produtos')
    
    # Converter para JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify(graphJSON)

@app.route('/api/sales_trend')
def sales_trend():
    period = request.args.get('period', 'month')
    
    if period == 'week':
        time_format = '%Y-%W'
        time_label = 'semana'
    elif period == 'day':
        time_format = '%Y-%m-%d'
        time_label = 'dia'
    else:  # month
        time_format = '%Y-%m'
        time_label = 'mês'
    
    query = f"""
    SELECT 
        strftime('{time_format}', date) as time_period,
        SUM(amount) as total_sales
    FROM sales
    GROUP BY time_period
    ORDER BY time_period
    """
    
    # Método 1: Usando pd.read_sql_query diretamente com o engine
    # df = pd.read_sql_query(text(query), engine)
    
    # Método 2 (alternativa): Usando execute() e DataFrame
    with engine.connect() as connection:
        result = connection.execute(text(query))
        df = pd.DataFrame(result.fetchall())
        df.columns = result.keys()
    
    # Criar gráfico com plotly
    fig = px.line(df, x='time_period', y='total_sales', title=f'Tendência de Vendas por {time_label.capitalize()}')
    
    # Converter para JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify(graphJSON)

if __name__ == '__main__':
    app.run(debug=True)