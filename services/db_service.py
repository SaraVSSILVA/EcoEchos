import sqlite3
import json
from passlib.context import CryptContext
import streamlit as st

# --- CONFIGURAÇÃO DE SENHA ---
# Define o esquema de criptografia. "bcrypt" é uma escolha forte e segura.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """Criptografa a senha em texto puro."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Verifica a senha em texto puro contra a sua versão criptografada."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Retorna False se o hash for inválido ou ocorrer outro erro, evitando que o app quebre.
        return False

# --- OPERAÇÕES DO BANCO DE DADOS ---
DB_NAME = 'users.db'

def init_db():
    """Inicializa o banco de dados e cria as tabelas se não existirem."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    # Tabela de dados mensais da pegada de carbono
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monthly_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            month_year TEXT NOT NULL,
            pegada_total REAL,
            input_data TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, month_year)
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password):
    """Registra um novo usuário com senha devidamente criptografada."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        # --- ESTA É A CORREÇÃO PRINCIPAL ---
        # A senha é criptografada ANTES de ser inserida no banco.
        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        st.success("Usuário registrado com sucesso! Agora você pode fazer o login.")
    except sqlite3.IntegrityError:
        st.error("Este nome de usuário já existe. Por favor, escolha outro.")
    finally:
        conn.close()

def login_user(username, password):
    """Faz o login do usuário, buscando no banco e verificando a senha criptografada."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
    user_record = cursor.fetchone()
    conn.close()

    if user_record and verify_password(password, user_record[2]): # user_record[2] é o password_hash
        return {'id': user_record[0], 'username': user_record[1]}
    else:
        st.error("Usuário ou senha inválidos.")
        return None

def save_user_monthly_data(user_id, month_year, pegada_total, input_data):
    """Salva ou atualiza os dados mensais de um usuário."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    input_data_json = json.dumps(input_data)
    try:
        # Usa ON CONFLICT para atualizar o registro se ele já existir (INSERT or UPDATE)
        cursor.execute('''
            INSERT INTO monthly_data (user_id, month_year, pegada_total, input_data)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, month_year) DO UPDATE SET
            pegada_total=excluded.pegada_total,
            input_data=excluded.input_data
        ''', (user_id, month_year, pegada_total, input_data_json))
        conn.commit()
        st.success(f"Dados de {month_year} salvos com sucesso!")
    finally:
        conn.close()

def load_user_monthly_data(user_id, month_year):
    """Carrega os dados mensais de um usuário a partir do banco de dados."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT pegada_total, input_data FROM monthly_data WHERE user_id = ? AND month_year = ?", (user_id, month_year))
    data_record = cursor.fetchone()
    conn.close()
    if data_record:
        return {'pegada_total': data_record[0], 'input_data': json.loads(data_record[1])}
    return None

