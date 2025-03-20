from flask import Flask, render_template, jsonify, request
import pandas as pd
import json
import plotly
import plotly.express as px
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Mude para uma chave secreta forte

# Configure o Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelo de usuário
class User(UserMixin):
    def __init__(self, id, email, password_hash):
        self.id = id
        self.email = email
        self.password_hash = password_hash

# Banco de dados de usuários simulado (substitua por um banco de dados real)
users = {}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Formulários
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

# Configuração do banco de dados
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///database/sales_data.db")
engine = create_engine(DATABASE_URI)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        
        # Procurar usuário pelo email
        user_id = None
        for uid, user_data in users.items():
            if user_data.email == email:
                user_id = uid
                break
        
        if user_id and check_password_hash(users[user_id].password_hash, form.password.data):
            login_user(users[user_id])
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Email ou senha inválidos')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        
        # Verificar se o email já está em uso
        if any(user.email == email for user in users.values()):
            flash('Este email já está registrado')
            return render_template('register.html', form=form)
        
        # Criar um novo usuário
        user_id = str(len(users) + 1)
        users[user_id] = User(
            id=user_id,
            email=email,
            password_hash=generate_password_hash(form.password.data)
        )
        
        flash('Conta criada com sucesso! Faça login para continuar.')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required

def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

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