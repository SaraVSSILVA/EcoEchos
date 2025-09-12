# 🎮 EcoEchos: O Eco das Suas Escolhas! 🌍🌱

Bem-vindo ao **EcoEchos**. Agora o projeto é centrado em uma API FastAPI (com autenticação JWT) e, opcionalmente, um cliente Streamlit local. Você pode:

- Calcular sua pegada de carbono por categorias (energia, transporte, alimentação, habitação, consumo, resíduos, estilo de vida).
- Salvar e carregar histórico diário e mensal por usuário.
- Usar gamificação: ranking mensal e conquistas por usuário.
- Integrar com frontend externo via REST (CORS configurável).

## ✨ Principais funcionalidades

- Autenticação JWT (login/cadastro de usuários)
- Endpoints em PT-BR para cálculo e histórico
- Banco de dados pluggable: SQLite (local) ou MongoDB Atlas (produção)
- Dicas de redução e fatores de emissão integrados
- Health check de banco: `/health/db`

## 🚀 Executar localmente (API)

### Pré-requisitos

- Python 3.10+ (recomendado 3.11)
- pip

### Instalação

```bash
python -m venv venv
./venv/Scripts/activate   # Windows
# source venv/bin/activate # macOS/Linux
pip install -r requirements.txt
```

### Configuração (.env)

- Para SQLite (mais simples):

```env
DB_BACKEND=SQLITE
SECRET_KEY=dev_key
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

- Para MongoDB Atlas (recomendado para persistência real):

```env
DB_BACKEND=MONGO
SECRET_KEY=dev_key
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
MONGODB_DBNAME=EcoEchosDB
MONGODB_USER=seu_usuario
MONGODB_PASSWORD=sua_senha
MONGODB_HOST=cluster0.seucluster.mongodb.net
MONGODB_APPNAME=EcoEchos
MONGODB_AUTH_SOURCE=admin
```

Observação: usando variáveis separadas, a API codifica usuário/senha automaticamente.

### Rodar API

```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8001
```

### Testar

- Docs (Swagger): <http://127.0.0.1:8001/docs>
- Health DB: <http://127.0.0.1:8001/health/db>

### Fluxo de uso (Swagger)

- POST /usuarios/registrar → cria usuário
- POST /autenticacao/entrar → pega access_token
- Authorize (Bearer token)
- POST /pegada/calcular → calcula a partir do JSON de inputs
- POST /historico/diario/salvar → salva um dia (não envie user_id; usa o do token)
- POST /historico/diario/carregar → carrega o dia
- POST /historico/mensal/carregar → soma do mês
- GET /ranking → ranking mensal
- GET /conquistas/{usuario_id} → conquistas do mês (use seu id do token ou GET /usuarios/eu)

## 🗄️ MongoDB Atlas (opcional)

Checklist:

- Database User com role readWrite no DB
- Network Access com seu IP liberado (para teste, 0.0.0.0/0)
- Conexão SRV do Atlas (host `.mongodb.net`)
- Se der “bad auth”: resetar senha, validar authSource, IP e URL-encoding (automático no modo de variáveis separadas)

## 🖥️ Cliente Streamlit (opcional/legado)

Se quiser usar o painel local como cliente offline (não integrado à API), basta:

```bash
streamlit run App.py
```

Observação: esse cliente usa o `db_service` (SQLite local) e não o backend FastAPI. Recomenda-se usar a API para dados unificados e gamificação completa.

## 📦 Deploy

- Projeto inclui Dockerfile, .dockerignore e Procfile (produção com Gunicorn/UvicornWorker)
- Health check: `/health/db`
- Para Render (sugestão), configure as variáveis de ambiente e aponte para o Dockerfile. Veja também `render.yaml` e `DEPLOY.md` para um guia rápido.

## �️ Estrutura do projeto (resumo)

- `api.py` → FastAPI (JWT, endpoints PT-BR, CORS, seleção de backend)
- `services/db_service.py` → SQLite
- `services/mongo_service.py` → MongoDB Atlas (PyMongo)
- `util/calculos_util.py` → cálculos de pegada
- `config/dicas.py`, `config/fatores_emissao.py` → dados de apoio
- `App.py` → Streamlit opcional (local/legado)
- `Dockerfile`, `.dockerignore`, `Procfile`, `render.yaml`, `DEPLOY.md`

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue / PR.

## 📄 Licença

MIT
