import os
import json
from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime

from passlib.context import CryptContext
from pymongo import ASCENDING, DESCENDING
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
import certifi


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


class MongoService:
    def __init__(self, uri: str, dbname: str):
        # Usa cadeia de certificados do certifi para evitar erros de TLS em ambientes minimalistas (ex.: Docker/Render)
        self.client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
        self.db = self.client[dbname]
        self.users: Collection = self.db["users"]
        self.daily: Collection = self.db["daily_data"]
        self.monthly: Collection = self.db["monthly_data"]
        try:
            self._ensure_indexes()
        except Exception:
            pass

    def _ensure_indexes(self):
        self.users.create_index([("username", ASCENDING)], unique=True)
        self.daily.create_index([("user_id", ASCENDING), ("date", ASCENDING)], unique=True)
        self.daily.create_index([("date", ASCENDING)])
        self.monthly.create_index([("user_id", ASCENDING), ("month_year", ASCENDING)], unique=True)

    def ping(self) -> bool:
        try:
            self.client.admin.command('ping')
            return True
        except Exception:
            return False

    # --- Usuários ---
    def register_user_api(self, username: str, password: str) -> Tuple[bool, str]:
        try:
            hashed = hash_password(password)
            self.users.insert_one({"username": username, "password_hash": hashed})
            return True, "Usuário cadastrado com sucesso!"
        except Exception as e:
            if "duplicate key" in str(e).lower():
                return False, "Este nome de usuário já existe. Por favor, escolha outro."
            return False, f"Erro ao cadastrar: {e}"

    def login_user_api(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        user = self.users.find_one({"username": username})
        if user and verify_password(password, user.get("password_hash", "")):
            return {"id": str(user["_id"]), "username": user["username"]}
        return None

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        from bson import ObjectId
        try:
            _id = ObjectId(user_id)
        except Exception:
            return None
        user = self.users.find_one({"_id": _id})
        if not user:
            return None
        return {"id": str(user["_id"]), "username": user["username"]}

    def update_user(self, user_id: str, new_username: Optional[str] = None, new_password: Optional[str] = None) -> Tuple[bool, str]:
        from bson import ObjectId
        try:
            _id = ObjectId(user_id)
        except Exception:
            return False, "Usuário inválido"
        update: Dict[str, Any] = {}
        if new_username is not None:
            update["username"] = new_username
        if new_password is not None:
            update["password_hash"] = hash_password(new_password)
        if not update:
            return False, "Nada para atualizar."
        try:
            self.users.update_one({"_id": _id}, {"$set": update})
            return True, "Usuário atualizado com sucesso!"
        except Exception as e:
            if "duplicate key" in str(e).lower():
                return False, "Este nome de usuário já está em uso."
            return False, f"Erro ao atualizar: {e}"

    # --- Histórico diário/mensal ---
    def save_user_daily_data(self, user_id: str, date: str, pegada_total: float, input_data: Dict[str, Any]):
        doc = {
            "user_id": user_id,
            "date": date,
            "pegada_total": float(pegada_total),
            "input_data": input_data,
            "updated_at": datetime.utcnow(),
        }
        self.daily.update_one({"user_id": user_id, "date": date}, {"$set": doc}, upsert=True)

    def load_user_daily_data(self, user_id: str, date: str) -> Optional[Dict[str, Any]]:
        doc = self.daily.find_one({"user_id": user_id, "date": date}, {"_id": 0})
        return doc

    def load_user_monthly_data(self, user_id: str, month_year: str) -> float:
        # Soma pegadas cujo date começa com YYYY-MM
        cur = self.daily.find({"user_id": user_id, "date": {"$regex": f"^{month_year}"}}, {"pegada_total": 1, "_id": 0})
        total = 0.0
        for d in cur:
            try:
                total += float(d.get("pegada_total", 0.0))
            except Exception:
                continue
        return total

    # --- Gamificação ---
    def get_monthly_ranking(self, month_year: str, limit: int = 10) -> List[Dict[str, Any]]:
        pipeline = [
            {"$match": {"date": {"$regex": f"^{month_year}"}}},
            {"$group": {"_id": "$user_id", "total": {"$sum": "$pegada_total"}}},
            {"$sort": {"total": -1}},
            {"$limit": int(limit)},
        ]
        agg = list(self.daily.aggregate(pipeline))
        ranking = []
        for r in agg:
            u = self.users.find_one({"_id": r["_id"]}) if False else None  # opcional: join manual
            ranking.append({
                "user_id": r["_id"],
                "username": None,  # para não encarecer a query; front pode resolver
                "total_pegada": float(r.get("total", 0.0)),
            })
        return ranking

    def get_user_achievements(self, user_id: str, month_year: str) -> Dict[str, Any]:
        cur = self.daily.find({"user_id": user_id, "date": {"$regex": f"^{month_year}"}}, {"input_data": 1, "_id": 0})
        days_logged = 0
        sum_bus_metro = 0.0
        sum_car_fuel_km = 0.0
        used_electric = False
        planted_trees = False
        for d in cur:
            days_logged += 1
            data = d.get("input_data", {}) or {}
            try:
                sum_bus_metro += float(data.get("km_onibus", 0.0)) + float(data.get("km_metro", 0.0))
                sum_car_fuel_km += float(data.get("distancia_carro_moto_combustivel", 0.0))
                if bool(data.get("usa_veiculo_eletrico", False)) and float(data.get("distancia_veiculo_eletrico", 0.0)) > 0:
                    used_electric = True
                if float(data.get("num_arvores_plantadas_mensal", 0.0)) > 0 or float(data.get("kg_creditos_carbono", 0.0)) > 0:
                    planted_trees = True
            except Exception:
                pass
        achievements = []
        achievements.append({"key": "registro_iniciado", "title": "Registro Iniciado", "achieved": days_logged >= 1, "details": f"{days_logged} dia(s) registrado(s)"})
        achievements.append({"key": "consistencia_bronze", "title": "Consistência Bronze", "achieved": days_logged >= 5})
        achievements.append({"key": "consistencia_prata", "title": "Consistência Prata", "achieved": days_logged >= 10})
        achievements.append({"key": "consistencia_ouro", "title": "Consistência Ouro", "achieved": days_logged >= 20})
        achievements.append({"key": "transporte_coletivo", "title": "Transporte Coletivo Adepto", "achieved": sum_bus_metro > sum_car_fuel_km})
        achievements.append({"key": "eletrificado", "title": "Eletrificado", "achieved": used_electric})
        achievements.append({"key": "plantador", "title": "Plantador/Compensador", "achieved": planted_trees})
        return {"month_year": month_year, "days_logged": days_logged, "achievements": achievements}
