from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus, urlparse

from util.calculos_util import calcular_pegada_completa
from services.db_service import (
    register_user_api as sqlite_register_user_api,
    login_user_api as sqlite_login_user_api,
    get_user_by_id as sqlite_get_user_by_id,
    update_user as sqlite_update_user,
    save_user_daily_data as sqlite_save_user_daily_data,
    load_user_daily_data as sqlite_load_user_daily_data,
    load_user_monthly_data as sqlite_load_user_monthly_data,
    get_monthly_ranking as sqlite_get_monthly_ranking,
    get_user_achievements as sqlite_get_user_achievements,
)
from services.mongo_service import MongoService
from config.dicas import DICAS_REDUCAO
from config.fatores_emissao import FATORES_EMISSAO

load_dotenv()

app = FastAPI()

# CORS
ALLOWED_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# MODELS
class UserRegisterRequest(BaseModel):
    username: str
    password: str


class UserLoginRequest(BaseModel):
    username: str
    password: str


class PegadaRequest(BaseModel):
    consumo_energia_kwh: float = 0.0
    num_botijoes_gas_13kg: float = 0.0
    distancia_carro_moto_combustivel: float = 0.0
    tipo_combustivel: str = "gasolina"
    usa_veiculo_eletrico: bool = False
    distancia_veiculo_eletrico: float = 0.0
    tipo_veiculo_eletrico: str = "carro_eletrico"
    km_onibus: float = 0.0
    km_metro: float = 0.0
    km_aviao_domestico: float = 0.0
    km_aviao_internacional: float = 0.0
    kg_carne_bovina: float = 0.0
    kg_carne_suina: float = 0.0
    kg_frango: float = 0.0
    kg_peixe: float = 0.0
    litros_leite: float = 0.0
    kg_queijo: float = 0.0
    duzias_ovo: int = 0
    kg_arroz: float = 0.0
    kg_feijao: float = 0.0
    kg_vegetais: float = 0.0
    num_comodos: int = 1
    horas_ar_condicionado_dia: float = 0.0
    horas_aquecedor_dia: float = 0.0
    num_celulares: float = 0.0
    num_laptops: float = 0.0
    num_geladeiras: float = 0.0
    num_televisoes: float = 0.0
    num_veiculos_eletricos_consumo: float = 0.0
    num_roupas_peca: float = 0.0
    num_sacos_lixo_100l: float = 0.0
    kg_lixo_reciclavel: float = 0.0
    kg_eletronico: float = 0.0
    kg_compostagem: float = 0.0
    num_voos_eventos_ano: int = 0
    horas_streaming_dia: float = 0.0
    num_compras_online_mes: int = 0
    num_arvores_plantadas_mensal: float = 0.0
    kg_creditos_carbono: float = 0.0


class SaveDailyDataRequest(BaseModel):
    user_id: Optional[int] = None  # Será validado contra o token, se presente
    date: str  # formato 'YYYY-MM-DD'
    pegada_total: float
    input_data: Dict[str, Any]


class LoadDailyDataRequest(BaseModel):
    user_id: Optional[int] = None
    date: str  # formato 'YYYY-MM-DD'


class LoadMonthlyDataRequest(BaseModel):
    user_id: Optional[int] = None
    month_year: str  # formato 'YYYY-MM'


class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


# --- JWT CONFIG ---
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_SECRET_KEY")  # Em produção, defina no ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24h

security = HTTPBearer(auto_error=True)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        # Não force conversão aqui; deixe cada backend lidar com o tipo (Mongo: str, SQLite: int)
        user_id = sub
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")

    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
    return user


# SAÚDE
@app.get("/")
def raiz():
    return {"mensagem": "API EcoEchos rodando!"}


@app.get("/health/db")
def health_db():
    try:
        if DB_BACKEND == "MONGO" and mongo:
            # ping no Mongo
            mongo.client.admin.command('ping')
            # Retorna algumas infos não sensíveis para ajudar no diagnóstico
            info = {"ok": True, "backend": "MONGO"}
            try:
                info.update(MONGO_CONN_INFO)
            except Exception:
                pass
            return info
        else:
            # verificação simples no SQLite via função já existente
            test = sqlite_get_user_by_id(-1)  # deve retornar None rapidamente
            return {"ok": True, "backend": "SQLITE"}
    except Exception as e:
        info = {"ok": False, "backend": DB_BACKEND, "error": str(e)}
        try:
            if DB_BACKEND == "MONGO":
                info.update(MONGO_CONN_INFO)
        except Exception:
            pass
        return info


"""
Seleção do backend de dados (SQLite ou MongoDB) via variável de ambiente DB_BACKEND.
Valores aceitos: 'MONGO' para MongoDB, qualquer outro valor -> SQLite.
"""
DB_BACKEND = os.getenv("DB_BACKEND", "SQLITE").upper()
mongo: Optional[MongoService] = None
MONGO_CONN_INFO: Dict[str, Any] = {}
if DB_BACKEND == "MONGO":
    MONGODB_URI = os.getenv("MONGODB_URI", "").strip()
    MONGODB_DBNAME = os.getenv("MONGODB_DBNAME", "ecoechos")
    # Permite construir a URI a partir de variáveis separadas, caso MONGODB_URI não esteja definida
    if not MONGODB_URI:
        MONGODB_USER = os.getenv("MONGODB_USER", "").strip()
        MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "").strip()
        MONGODB_HOST = os.getenv("MONGODB_HOST", "").strip()  # ex.: cluster0.xxxxx.mongodb.net
        MONGODB_APPNAME = os.getenv("MONGODB_APPNAME", "EcoEchos").strip()
        MONGODB_AUTH_SOURCE = os.getenv("MONGODB_AUTH_SOURCE", "admin").strip()
        MONGODB_AUTH_MECH = os.getenv("MONGODB_AUTH_MECH", "").strip()  # opcional, ex.: SCRAM-SHA-256
        if MONGODB_USER and MONGODB_PASSWORD and MONGODB_HOST:
            mech_q = f"&authMechanism={MONGODB_AUTH_MECH}" if MONGODB_AUTH_MECH else ""
            MONGODB_URI = (
                f"mongodb+srv://{quote_plus(MONGODB_USER)}:{quote_plus(MONGODB_PASSWORD)}@{MONGODB_HOST}/"
                f"?retryWrites=true&w=majority&appName={MONGODB_APPNAME}&authSource={MONGODB_AUTH_SOURCE}{mech_q}"
            )
    if not MONGODB_URI:
        raise RuntimeError("MONGODB_URI não definido e variáveis (MONGODB_USER, MONGODB_PASSWORD, MONGODB_HOST) ausentes")
    # Prepara informações não sensíveis para health
    mode = "URI" if os.getenv("MONGODB_URI", "").strip() else "COMPONENTS"
    host = ""
    try:
        # tentativa simples de extrair host a partir da URI
        netloc = MONGODB_URI.split("@")[1] if "@" in MONGODB_URI else urlparse(MONGODB_URI).netloc
        host = netloc.split("/")[0].split("?")[0]
    except Exception:
        host = ""
    MONGO_CONN_INFO = {
        "mode": mode,
        "host": host,
        "dbname": MONGODB_DBNAME,
        "appName": os.getenv("MONGODB_APPNAME", "EcoEchos").strip(),
        "authSource": os.getenv("MONGODB_AUTH_SOURCE", "admin").strip(),
        "authMechanism": os.getenv("MONGODB_AUTH_MECH", "").strip() or None,
    }
    mongo = MongoService(MONGODB_URI, MONGODB_DBNAME)


def as_user_id(value: Any) -> str:
    """Converte IDs em string quando Mongo está ativo; SQLite usa int, mas tratamos como str para token."""
    return str(value)


def register_user_api(username: str, password: str):
    if DB_BACKEND == "MONGO" and mongo:
        return mongo.register_user_api(username, password)
    return sqlite_register_user_api(username, password)


def login_user_api(username: str, password: str) -> Optional[Dict[str, Any]]:
    if DB_BACKEND == "MONGO" and mongo:
        return mongo.login_user_api(username, password)
    return sqlite_login_user_api(username, password)


def get_user_by_id(user_id: Any) -> Optional[Dict[str, Any]]:
    if DB_BACKEND == "MONGO" and mongo:
        return mongo.get_user_by_id(str(user_id))
    return sqlite_get_user_by_id(int(user_id))


def update_user(user_id: Any, new_username: Optional[str] = None, new_password: Optional[str] = None):
    if DB_BACKEND == "MONGO" and mongo:
        return mongo.update_user(str(user_id), new_username, new_password)
    return sqlite_update_user(int(user_id), new_username, new_password)


def save_user_daily_data(user_id: Any, date: str, pegada_total: float, input_data: Dict[str, Any]):
    if DB_BACKEND == "MONGO" and mongo:
        return mongo.save_user_daily_data(str(user_id), date, pegada_total, input_data)
    return sqlite_save_user_daily_data(int(user_id), date, pegada_total, input_data)


def load_user_daily_data(user_id: Any, date: str) -> Optional[Dict[str, Any]]:
    if DB_BACKEND == "MONGO" and mongo:
        return mongo.load_user_daily_data(str(user_id), date)
    data = sqlite_load_user_daily_data(int(user_id), date)
    return data


def load_user_monthly_data(user_id: Any, month_year: str) -> float:
    if DB_BACKEND == "MONGO" and mongo:
        return mongo.load_user_monthly_data(str(user_id), month_year)
    return sqlite_load_user_monthly_data(int(user_id), month_year)


def get_monthly_ranking(month_year: str, limit: int = 10):
    if DB_BACKEND == "MONGO" and mongo:
        return mongo.get_monthly_ranking(month_year, limit)
    return sqlite_get_monthly_ranking(month_year, limit)


def get_user_achievements(user_id: Any, month_year: str):
    if DB_BACKEND == "MONGO" and mongo:
        return mongo.get_user_achievements(str(user_id), month_year)
    return sqlite_get_user_achievements(int(user_id), month_year)
@app.post("/usuarios/registrar")
def registrar_usuario(req: UserRegisterRequest):
    ok, msg = register_user_api(req.username, req.password)
    return {"success": ok, "message": msg}


@app.post("/autenticacao/entrar")
def entrar(req: UserLoginRequest):
    user_data = login_user_api(req.username, req.password)
    if user_data:
        # Gera token JWT
        access_token = create_access_token({"sub": str(user_data["id"]), "username": user_data["username"]})
        return {"success": True, "access_token": access_token, "token_type": "bearer", "user": user_data}
    else:
        return {"success": False, "message": "Usuário ou senha inválidos."}


@app.get("/usuarios/{usuario_id}")
def obter_usuario(usuario_id: int, current_user: Dict[str, Any] = Depends(get_current_user)):
    if str(current_user["id"]) != str(usuario_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
    data = get_user_by_id(usuario_id)
    if data:
        return {"success": True, "user": data}
    return {"success": False, "message": "Usuário não encontrado."}


@app.get("/usuarios/eu")
def eu(current_user: Dict[str, Any] = Depends(get_current_user)):
    return {"success": True, "user": current_user}


@app.put("/usuarios/{usuario_id}")
def atualizar_usuario(usuario_id: int, req: UserUpdateRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    if str(current_user["id"]) != str(usuario_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
    ok, msg = update_user(usuario_id, req.username, req.password)
    return {"success": ok, "message": msg}


# CÁLCULO
@app.post("/pegada/calcular")
def calcular_pegada(req: PegadaRequest):
    resultado = calcular_pegada_completa(req.dict())
    return resultado


# HISTÓRICO
@app.post("/historico/diario/salvar")
def salvar_historico_diario(req: SaveDailyDataRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    try:
        # Valida/usa o user_id do token
        user_id = current_user["id"] if req.user_id is None else req.user_id
        if str(user_id) != str(current_user["id"]):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
        save_user_daily_data(user_id, req.date, req.pegada_total, req.input_data)
        return {"success": True, "message": "Dados salvos com sucesso!"}
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.post("/historico/diario/carregar")
def carregar_historico_diario(req: LoadDailyDataRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    try:
        user_id = current_user["id"] if req.user_id is None else req.user_id
        if str(user_id) != str(current_user["id"]):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
        dados = load_user_daily_data(user_id, req.date)
        if dados:
            return {"success": True, "data": dados}
        else:
            return {"success": False, "message": "Nenhum dado encontrado para esta data."}
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.post("/historico/mensal/carregar")
def carregar_historico_mensal(req: LoadMonthlyDataRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    try:
        user_id = current_user["id"] if req.user_id is None else req.user_id
        if str(user_id) != str(current_user["id"]):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
        dados = load_user_monthly_data(user_id, req.month_year)
        if dados is not None:
            return {"success": True, "data": dados}
        else:
            return {"success": False, "message": "Nenhum dado encontrado para este mês."}
    except Exception as e:
        return {"success": False, "message": str(e)}


# DADOS DE CONFIG
@app.get("/dicas")
def obter_dicas():
    return {"dicas": DICAS_REDUCAO}


@app.get("/fatores-emissao")
def obter_fatores_emissao():
    return {"fatores_emissao": FATORES_EMISSAO}


# GAMIFICAÇÃO
@app.get("/ranking")
def ranking(month_year: str, limit: int = 10):
    """Ranking por mês (maior pegada total primeiro). Parâmetros via query."""
    data = get_monthly_ranking(month_year, limit)
    return {"success": True, "month_year": month_year, "ranking": data}


@app.get("/conquistas/{usuario_id}")
def conquistas(usuario_id: int, month_year: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    if current_user["id"] != usuario_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
    data = get_user_achievements(usuario_id, month_year)
    return {"success": True, **data}


# Para rodar: uvicorn api:app --reload
# Docs: http://localhost:8000/docs
