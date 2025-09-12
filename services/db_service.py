import sqlite3
import json
from passlib.context import CryptContext
from typing import Optional, Tuple, Dict, Any

# Importa Streamlit apenas se disponível (para uso na interface antiga)
try:
    import streamlit as st  # type: ignore
except Exception:  # pragma: no cover
    st = None  # Permite rodar API sem depender de Streamlit

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
            data TEXT,
            pegada_total REAL,
            input_data TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, data)
        )
    ''')
    # Tabela de dados diários da pegada de carbono
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            pegada_total REAL,
            input_data TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, date)
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password):
    """Registra um novo usuário com senha devidamente criptografada."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        if st:
            st.success("Usuário registrado com sucesso! Agora você pode fazer o login.")
    except sqlite3.IntegrityError:
        if st:
            st.error("Este nome de usuário já existe. Por favor, escolha outro.")
    finally:
        conn.close()

# --- Funções sem dependência de Streamlit (para API) ---
def register_user_api(username: str, password: str) -> Tuple[bool, str]:
    """Registra um novo usuário (uso pela API). Retorna (sucesso, mensagem)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        return True, "Usuário cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Este nome de usuário já existe. Por favor, escolha outro."
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
        if st:
            st.error("Usuário ou senha inválidos.")
        return None

def login_user_api(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Login sem dependência de Streamlit (uso pela API)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
    user_record = cursor.fetchone()
    conn.close()
    if user_record and verify_password(password, user_record[2]):
        return {"id": user_record[0], "username": user_record[1]}
    return None

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1]}
    return None

def update_user(user_id: int, new_username: Optional[str] = None, new_password: Optional[str] = None) -> Tuple[bool, str]:
    """Atualiza username e/ou password; retorna (sucesso, mensagem)."""
    if new_username is None and new_password is None:
        return False, "Nada para atualizar."
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        if new_username is not None:
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
        if new_password is not None:
            hashed = hash_password(new_password)
            cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hashed, user_id))
        conn.commit()
        return True, "Usuário atualizado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Este nome de usuário já está em uso."
    finally:
        conn.close()

def save_user_daily_data(user_id, date, pegada_total, input_data):
    """Salva ou atualiza os dados mensais de um usuário."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    input_data_json = json.dumps(input_data)
    try:
        # Usa ON CONFLICT para atualizar o registro se ele já existir (INSERT or UPDATE)
        cursor.execute('''
            INSERT INTO daily_data (user_id, date, pegada_total, input_data)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, date) DO UPDATE SET
            pegada_total=excluded.pegada_total,
            input_data=excluded.input_data
        ''', (user_id, date, pegada_total, input_data_json))
        conn.commit()
        if st:
            st.success(f"Dados de {date} salvos com sucesso!")
    finally:
        conn.close()

def load_user_daily_data(user_id, date):
    """Carrega os dados mensais de um usuário a partir do banco de dados."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT pegada_total, input_data FROM daily_data WHERE user_id = ? AND date = ?", (user_id, date))
    data_record = cursor.fetchone()
    conn.close()
    if data_record:
        return {'pegada_total': data_record[0], 'input_data': json.loads(data_record[1])}
    return None

def load_user_monthly_data(user_id, month_year):
    """Carrega e soma os dados diários de um mês específico."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT pegada_total FROM daily_data WHERE user_id = ? AND date LIKE ?", (user_id, f"{month_year}%"))

    pegadas_diarias = cursor.fetchall()
    conn.close()

    if pegadas_diarias:
        pegada_total_mensal = sum(p[0] for p in pegadas_diarias)
        return pegada_total_mensal
    return 0.0

# --- Gamificação: Ranking e Conquistas ---
def get_monthly_ranking(month_year: str, limit: int = 10):
    """Retorna ranking dos usuários pela soma de pegada_total no mês (maior para menor)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT u.id, u.username, COALESCE(SUM(d.pegada_total), 0) as total
        FROM users u
        LEFT JOIN daily_data d ON u.id = d.user_id AND d.date LIKE ?
        GROUP BY u.id, u.username
        ORDER BY total DESC
        LIMIT ?
        ''', (f"{month_year}%", limit)
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {"user_id": r[0], "username": r[1], "total_pegada": r[2]}
        for r in rows
    ]

def get_user_achievements(user_id: int, month_year: str):
    """Gera conquistas simples com base nos dados diários do mês.
    Exemplos: consistência (n dias logados), uso de transporte coletivo/elétrico, ações sustentáveis.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT date, pegada_total, input_data FROM daily_data WHERE user_id = ? AND date LIKE ?",
        (user_id, f"{month_year}%")
    )
    rows = cursor.fetchall()
    conn.close()

    days_logged = len(rows)
    sum_bus_metro = 0.0
    sum_car_fuel_km = 0.0
    used_electric = False
    planted_trees = False

    for _, _, input_json in rows:
        try:
            data = json.loads(input_json) if isinstance(input_json, str) else (input_json or {})
        except Exception:
            data = {}
        sum_bus_metro += float(data.get("km_onibus", 0.0)) + float(data.get("km_metro", 0.0))
        sum_car_fuel_km += float(data.get("distancia_carro_moto_combustivel", 0.0))
        if bool(data.get("usa_veiculo_eletrico", False)) and float(data.get("distancia_veiculo_eletrico", 0.0)) > 0:
            used_electric = True
        if float(data.get("num_arvores_plantadas_mensal", 0.0)) > 0 or float(data.get("kg_creditos_carbono", 0.0)) > 0:
            planted_trees = True

    achievements = []
    # Registro iniciado
    achievements.append({"key": "registro_iniciado", "title": "Registro Iniciado", "achieved": days_logged >= 1, "details": f"{days_logged} dia(s) registrado(s)"})
    # Consistência níveis
    achievements.append({"key": "consistencia_bronze", "title": "Consistência Bronze", "achieved": days_logged >= 5})
    achievements.append({"key": "consistencia_prata", "title": "Consistência Prata", "achieved": days_logged >= 10})
    achievements.append({"key": "consistencia_ouro", "title": "Consistência Ouro", "achieved": days_logged >= 20})
    # Preferência por coletivo
    achievements.append({"key": "transporte_coletivo", "title": "Transporte Coletivo Adepto", "achieved": sum_bus_metro > sum_car_fuel_km})
    # Uso de elétrico
    achievements.append({"key": "eletrificado", "title": "Eletrificado", "achieved": used_electric})
    # Ações sustentáveis
    achievements.append({"key": "plantador", "title": "Plantador/Compensador", "achieved": planted_trees})

    return {
        "month_year": month_year,
        "days_logged": days_logged,
        "achievements": achievements
    }


    


    

