<div align="center">

# 💰 Control Expenses API

**API REST para controle de gastos pessoais**, com autenticação em duas camadas (access + refresh token via JWT), senhas protegidas com bcrypt e persistência em PostgreSQL.

<p>
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-0.141-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT"/>
  <img src="https://img.shields.io/badge/Bcrypt-8A2BE2?style=for-the-badge" alt="Bcrypt"/>
  <img src="https://img.shields.io/badge/Uvicorn-2A2A2A?style=for-the-badge" alt="Uvicorn"/>
  <img src="https://img.shields.io/badge/license-unspecified-lightgrey?style=for-the-badge" alt="License"/>
</p>

</div>

---

## 📑 Índice

- [Sobre o projeto](#-sobre-o-projeto)
- [Novidades desta versão](#-novidades-desta-versão)
- [Arquitetura](#-arquitetura)
- [Estrutura de pastas](#-estrutura-de-pastas)
- [Tecnologias](#-tecnologias)
- [Autenticação](#-autenticação)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração](#%EF%B8%8F-configuração)
- [Como executar](#-como-executar)
- [Rotas da API](#%EF%B8%8F-rotas-da-api)
  - [Auth](#-auth-auth)
  - [Users](#-users-users)
  - [Expanses](#-expanses-expanses)
- [Modelo de dados](#%EF%B8%8F-modelo-de-dados)
- [Logs](#-logs)
- [Limitações conhecidas](#-limitações-conhecidas)

---

## 📌 Sobre o projeto

O **Control Expenses** é uma API construída em **FastAPI** para que cada usuário cadastre, consulte, atualize e remova seus próprios gastos (nome, quantidade e preço), com o total calculado automaticamente (`quantity * price`). Cada gasto pertence a um usuário autenticado, identificado a partir do JWT emitido no login.

---

## 🆕 Novidades desta versão

Em relação à versão anterior do projeto, esta release trouxe melhorias relevantes de segurança e organização:

- **Rota `/auth` dedicada**: login, logout e refresh de token deixaram de ficar misturados em `/users` e agora têm seu próprio router.
- **Access token + Refresh token**: o login agora emite dois cookies (`user_token`, de curta duração, e `user_refresh_token`), permitindo renovar a sessão sem pedir a senha novamente.
- **Expiração de token**: o access token carrega um campo `expired` e o middleware valida se ele já expirou antes de processar a requisição.
- **CORS restrito por domínio**: `allow_origins` deixou de ser `"*"` e passou a usar a variável de ambiente `domain`, corrigindo a combinação insegura anterior com `allow_credentials=True`.
- **`requirements.txt` corrigido**: agora lista apenas as dependências reais do projeto, com versões fixas (antes continha um *pip freeze* de sistema, com pacotes não relacionados).
- **Imports absolutos com prefixo `src.`**: todo o projeto foi migrado para importar módulos como `src.controller...`, `src.domain...`, etc., tornando a execução via `python -m` mais previsível.
- **Middleware reescrito**: `ValidMidlleware` agora retorna um dicionário estruturado (`{"error", "status_code"}`) em vez de lançar exceções soltas, e consegue injetar o token renovado na resposta.
- **Busca de usuário parametrizada corretamente**: `UsersDb.select` agora recebe `search` (`"email"` ou `"public_id"`) e `value` separadamente, eliminando a tentativa anterior de parametrizar nome de coluna via bind param (que não é suportado pelo SQLAlchemy).

---

## 🏗️ Arquitetura

O projeto mantém a **arquitetura em camadas**, onde cada módulo depende apenas da camada abaixo dele:

```
Controller  → recebe a requisição HTTP, define rotas, middleware global e dependências
     ↓
Service     → camada de "montagem": une domain + repository + infra em instâncias prontas para uso
     ↓
Domain      → regras de negócio, validação de dados (Pydantic) e criptografia (JWT/hash)
     ↓
Repository  → acesso a dados, executa as queries SQL via SQLAlchemy
     ↓
Infra       → configuração (variáveis de ambiente), conexão com o banco e criação de tabelas
```

### Fluxo de autenticação (login → requisição autenticada)

```
1. Cliente faz POST /auth
     └─ valida e-mail/senha → gera access token (JWT, expira em 3 dias)
                             → gera refresh token (JWT)
     └─ ambos são salvos em cookies httpOnly ("user_token" e "user_refresh_token")

2. Cliente faz requisições subsequentes enviando o cookie "user_token"
     │
     ▼
   Middleware global (Midlleware)
     ├─ roda apenas lógica extra para rotas /users/*
     ├─ verifica se o token expirou (ValidUsers.expired)
     ├─ verifica regras de negócio (usuário existe / não existe / senha confere)
     └─ se tudo OK, repassa a requisição adiante (call_next)

3. Rotas de /expanses usam Depends(depends)
     └─ service/depends.py (GetUser) decodifica o cookie e resolve o "id" interno do usuário

4. Quando o access token expirar, o cliente chama PATCH /auth
     └─ usa o refresh token para emitir um novo par de tokens, sem precisar logar de novo
```

### Responsabilidade de cada camada

| Camada | Pasta | Responsabilidade |
|---|---|---|
| **Controller** | `src/controller` | Define os `APIRouter` (`/auth`, `/users`, `/expanses`), o middleware global e a instância principal do FastAPI (`Main`). |
| **Service** | `src/service` | "Cola" as camadas — instancia `ControlDb`, `JwtToken`, `HashPass` e `GetUser`, prontos para uso nos controllers. |
| **Domain** | `src/domain` | *Models* Pydantic (validação de entrada), regras de negócio de usuário (`ValidUsers`) e classes de criptografia (`JwtToken`, `HashPass`). |
| **Repository** | `src/repository` | Executa as queries SQL (raw SQL via `sqlalchemy.text`) para as tabelas `users` e `expanses`. |
| **Infra** | `src/infra` | Carrega variáveis de ambiente (`url`, `sing`, `domain`), cria a `Engine` do SQLAlchemy e o schema do banco (`start_schema`). |
| **Logs** | `src/logs` | Configuração global de logging (arquivo `app.log` + `stdout`), usada em praticamente todas as camadas. |

---

## 📂 Estrutura de pastas

```
Control_expenses/
├── README.md
├── config/
│   ├── Dockerfile               # imagem da API (Python 3.11)
│   ├── docker-compose.yml       # orquestração do container da API
│   └── requirements.txt         # dependências reais do projeto, com versões fixas
│
└── src/
    ├── controller/
    │   ├── main.py                # cria e configura a instância FastAPI
    │   ├── dependences/
    │   │   └── depends.py         # dependência de autenticação usada em /expanses
    │   ├── midllewares/
    │   │   └── users.py           # middleware HTTP: valida regras + renova cookie de token
    │   └── handles/
    │       ├── auth.py            # login, logout e refresh de token (/auth)
    │       ├── users.py           # criação, atualização e exclusão de conta (/users)
    │       └── expanses.py        # CRUD de gastos (/expanses)
    │
    ├── service/
    │   ├── manage.py               # agrega db, jwt, hash, middleware e depends
    │   ├── db.py                   # instancia o ControlDb com a engine
    │   ├── depends.py              # GetUser: extrai o usuário autenticado do token
    │   ├── encode.py                # instancia JwtToken e HashPass com a chave (sing)
    │   └── midleware.py            # ValidMidlleware: liga o middleware às regras de negócio
    │
    ├── domain/
    │   ├── module.py                # ponto único de importação dos módulos do domínio
    │   ├── models/
    │   │   ├── model_user.py        # validação de usuário (senha, e-mail, login, update)
    │   │   └── model_expanses.py    # validação de gastos
    │   ├── role/
    │   │   └── users.py             # regra de negócio: existe/não existe/senha válida/expiração
    │   └── encode/
    │       ├── jwt.py               # criação e leitura de tokens JWT
    │       └── hash.py              # hash e verificação de senha com bcrypt
    │
    ├── repository/
    │   ├── manage.py                # ControlDb: agrega UsersDb e ExpansesDb
    │   └── db/
    │       ├── users.py             # CRUD SQL da tabela users
    │       └── expanses.py          # CRUD SQL da tabela expanses
    │
    ├── infra/
    │   ├── manage.py                # cria a engine do banco / comando start_schema
    │   ├── core/
    │   │   ├── settings.py          # carrega variáveis de ambiente (.env)
    │   │   ├── security.py          # regras de rota protegidas por método/path
    │   │   └── .env                 # variáveis de ambiente (não versionar em produção)
    │   └── database/
    │       ├── connection.py        # cria e testa a conexão (Engine) com o PostgreSQL
    │       └── tables.py            # cria as tabelas users e expanses caso não existam
    │
    └── logs/
        ├── log.py                   # configuração do logger (arquivo + console)
        └── app.log                   # arquivo de log gerado em runtime
```

---

## 🧰 Tecnologias

| Categoria | Tecnologia | Uso no projeto |
|---|---|---|
| Linguagem | **Python 3.11** | Runtime da aplicação (imagem Docker `python:3.11`) |
| Framework web | **FastAPI 0.141** | Roteamento, validação automática, middlewares |
| Servidor ASGI | **Uvicorn** | Executa a aplicação FastAPI |
| ORM/Toolkit SQL | **SQLAlchemy 2.0** | Engine de conexão e execução das queries |
| Driver PostgreSQL | **psycopg2** | Comunicação com o banco |
| Banco de dados | **PostgreSQL** | Persistência (`serial`, `uuid`, `timestamptz`) |
| Validação | **Pydantic 2** | Validação de payloads e regras de formato (senha, e-mail) |
| Autenticação | **PyJWT** | Geração e leitura de tokens (access + refresh), algoritmo `HS256` |
| Segurança de senha | **bcrypt** | Hash e verificação de senhas |
| Configuração | **python-dotenv** | Carregamento de variáveis de ambiente do `.env` |
| Containerização | **Docker / Docker Compose** | Build e execução da API isolada |

---

## 🔐 Autenticação

O projeto usa um esquema de **dois tokens JWT**, ambos em cookies `httpOnly` + `SameSite=Strict`:

| Cookie | Função | Emitido em |
|---|---|---|
| `user_token` | Access token — usado para autorizar requisições | `POST /auth` (login) e `POST /users` (cadastro) |
| `user_refresh_token` | Refresh token — usado para renovar o access token sem nova senha | `POST /auth` (login) e `POST /users` (cadastro) |

O access token carrega `public_id`, `name`, `role`, uma data de expiração (`expired`, 3 dias após emissão) e `type: "acess"`. O refresh token carrega `type: "refresh"`.

**Middleware global** (`controller/midllewares/users.py`): intercepta toda requisição e, especificamente para o prefixo `/users/`, aplica regras adicionais de negócio (`domain/role/users.py`):
- Bloqueia cadastro se o e-mail já existir.
- Bloqueia update/delete se o usuário não existir.
- Verifica se a senha enviada confere com o hash salvo.
- Verifica se o access token já expirou.

**Rotas `/expanses`** usam uma dependência própria (`Depends(depends)`) que lê o cookie `user_token`, decodifica o JWT e resolve o `id` interno do usuário para vincular os gastos a ele.

> ℹ️ As rotas `PATCH /users` e `DELETE /users` esperam o token no **header** `X-user_token`, enquanto o login (`/auth`) e as rotas de gastos (`/expanses`) usam o **cookie** `user_token`. Ao consumir a API, envie o token da forma que a rota específica espera (ver seção de rotas abaixo).

---

## ✅ Pré-requisitos

- Python 3.11+ (ou Docker)
- Uma instância PostgreSQL acessível
- Docker e Docker Compose (opcional, para rodar containerizado)

---

## ⚙️ Configuração

Crie o arquivo `src/infra/core/.env` com as seguintes variáveis:

```env
url=postgresql+psycopg2://usuario:senha@host:5432/nome_do_banco
sing=uma-chave-secreta-forte-para-assinar-o-jwt
domain=http://localhost:3000
```

| Variável | Descrição |
|---|---|
| `url` | String de conexão do SQLAlchemy com o PostgreSQL |
| `sing` | Chave secreta usada para assinar/validar os tokens JWT (algoritmo `HS256`) |
| `domain` | Origem (frontend) autorizada pelo CORS a consumir a API com credenciais |

---

## 🚀 Como executar

### Opção 1 — Docker (recomendado)

```bash
git clone https://github.com/BrayanDevZN/Control_expenses.git
cd Control_expenses
docker compose -f config/docker-compose.yml up --build
```

A API sobe em `http://localhost:8000`. O próprio container cria o schema antes de iniciar o servidor:

```bash
python -m src.infra.manage start_schema && python -m uvicorn src.controller.main:app --host 0.0.0.0 --port 8000
```

### Opção 2 — Ambiente local

```bash
git clone https://github.com/BrayanDevZN/Control_expenses.git
cd Control_expenses

# criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# instalar dependências
pip install -r config/requirements.txt

# criar as tabelas no banco
python -m src.infra.manage start_schema

# iniciar a API
python -m uvicorn src.controller.main:app --reload --port 8000
```

Documentação interativa gerada automaticamente pelo FastAPI:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🛣️ Rotas da API

### 🔑 Auth (`/auth`)

| Método | Rota | Autenticação | Descrição |
|---|---|---|---|
| `POST` | `/auth/` | Não | Login — valida e-mail/senha e emite `user_token` + `user_refresh_token` |
| `DELETE` | `/auth/` | Não | Logout — remove o cookie `user_token` |
| `PATCH` | `/auth/` | Cookies `user_token` + `user_refresh_token` | Renova o access token usando o refresh token |

<details>
<summary><strong>POST /auth/</strong> — Login</summary>

**Body**
```json
{
  "email": "brayan@gmail.com",
  "password": "Senha123"
}
```

**Resposta** `200 OK`
```json
{
  "name": "Brayan Dev",
  "created_at": "2026-08-10T12:00:00Z"
}
```
Cookies `user_token` e `user_refresh_token` são definidos na resposta.
Erros: `401` (usuário não encontrado), `422` (senha inválida).
</details>

<details>
<summary><strong>DELETE /auth/</strong> — Logout</summary>

Remove o cookie `user_token`. Não requer body.

**Resposta**
```json
{ "status": "sucess" }
```
</details>

<details>
<summary><strong>PATCH /auth/</strong> — Renovar token</summary>

Requer os cookies `user_token` (mesmo expirado) e `user_refresh_token` válidos.

**Resposta**
```json
{ "status": "sucess" }
```
Emite um novo `user_token` e `user_refresh_token`.
</details>

---

### 👤 Users (`/users`)

| Método | Rota | Autenticação | Descrição |
|---|---|---|---|
| `POST` | `/users/` | Não | Cria uma nova conta e já emite `user_token` + `user_refresh_token` |
| `PATCH` | `/users/` | Header `X-user_token` | Atualiza a senha do usuário autenticado |
| `DELETE` | `/users/` | Header `X-user_token` | Remove a conta do usuário autenticado |

**Regras de validação** (`domain/models/model_user.py`):
- **E-mail**: deve conter `@gmail.com`.
- **Senha**: mínimo 8 caracteres, com ao menos 1 letra maiúscula, 1 minúscula e 1 dígito.

<details>
<summary><strong>POST /users/</strong> — Criar conta</summary>

**Body**
```json
{
  "name": "Brayan Dev",
  "email": "brayan@gmail.com",
  "password": "Senha123"
}
```

**Resposta** `200 OK`
```json
{
  "name": "Brayan Dev",
  "created_at": "2026-08-10T12:00:00Z"
}
```
Cookies `user_token` e `user_refresh_token` são definidos na resposta. A conta é criada com `role="user"` por padrão.
</details>

<details>
<summary><strong>PATCH /users/</strong> — Atualizar senha</summary>

**Header:** `X-user_token: <jwt>`

**Body**
```json
{
  "password": "SenhaAtual123",
  "new_password": "SenhaNova456"
}
```

Se `new_password` for igual a `password`, retorna `501` com `{"detail": "invalid password"}`. Em caso de sucesso, o cookie `user_token` atual é removido (é necessário logar novamente).
</details>

<details>
<summary><strong>DELETE /users/</strong> — Excluir conta</summary>

**Header:** `X-user_token: <jwt>`

**Body**
```json
{
  "password": "SenhaAtual123"
}
```

**Resposta**: `201` + `{"status": "sucess"}`, e o cookie `user_token` é removido.
</details>

---

### 💸 Expanses (`/expanses`)

Todas as rotas abaixo exigem o cookie `user_token` — o `user_id` é resolvido automaticamente a partir do token.

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/expanses/` | Cria um novo gasto para o usuário autenticado |
| `GET` | `/expanses/` | Lista os gastos do usuário (ou busca um específico pelo `name`) |
| `PATCH` | `/expanses/` | Atualiza um campo (`name`, `quantity` ou `price`) de um gasto |
| `DELETE` | `/expanses/` | Remove um gasto (ou todos, se `name` não for informado) |

<details>
<summary><strong>POST /expanses/</strong> — Criar gasto</summary>

**Body**
```json
{
  "name": "Mercado",
  "quantity": 3,
  "price": 45.90
}
```

**Resposta**
```json
{
  "id": 1,
  "user_id": 4,
  "name": "Mercado",
  "quantity": 3,
  "price": 45.90,
  "total": 137.70
}
```

`quantity` e `price` devem ser maiores que zero. Retorna erro se já existir um gasto com o mesmo nome para o usuário.
</details>

<details>
<summary><strong>GET /expanses/?name=Mercado</strong> — Listar / buscar gastos</summary>

- Sem `name`: retorna **todos** os gastos do usuário autenticado.
- Com `name`: retorna o gasto específico (ou `401` se não encontrado).

**Resposta**
```json
{
  "name": "Mercado",
  "quantity": 3,
  "price": 45.90,
  "total": 137.70
}
```
</details>

<details>
<summary><strong>PATCH /expanses/</strong> — Atualizar gasto</summary>

**Body**
```json
{
  "name": "Mercado",
  "set": "price",
  "value": 52.30
}
```

`set` aceita apenas: `"name"`, `"quantity"` ou `"price"`.
</details>

<details>
<summary><strong>DELETE /expanses/?name=Mercado</strong> — Remover gasto</summary>

Remove o gasto informado em `name` (ou todos os gastos do usuário, se omitido).

**Resposta**
```json
{ "status": "sucess" }
```
</details>

---

## 🗄️ Modelo de dados

### `users`

| Coluna | Tipo | Observação |
|---|---|---|
| `id` | `serial` | Chave primária |
| `public_id` | `uuid` | Identificador público, usado no payload do JWT |
| `name` | `text` | Nome do usuário |
| `email` | `text` | E-mail (login) |
| `password` | `text` | Hash bcrypt da senha |
| `role` | `text` | Papel do usuário (padrão: `"user"`) |
| `wage` | `numeric(10,2)` | Campo opcional |
| `created_at` | `timestamptz` | Data de criação |

### `expanses`

| Coluna | Tipo | Observação |
|---|---|---|
| `id` | `serial` | Chave primária |
| `user_id` | `int` | FK → `users.id` (`on delete cascade`) |
| `name` | `text` | Nome do gasto (único) |
| `quantity` | `int` | Quantidade |
| `price` | `numeric(10,2)` | Preço unitário |
| `created_at` | `timestamptz` | Data de criação |

> As tabelas são criadas automaticamente ao rodar `python -m src.infra.manage start_schema` (comando já incluído no `CMD` do Dockerfile).

---

## 📝 Logs

Toda a aplicação usa um logger centralizado (`src/logs/log.py`) que grava simultaneamente:
- No console (`stdout`)
- No arquivo `src/logs/app.log`

Formato: `AAAA-MM-DD HH:MM:SS [NÍVEL] mensagem`

---

## ⚠️ Limitações conhecidas

- A dependência de `/expanses` (`GetUser`) busca o usuário passando só o `public_id` para `UsersDb.select`, que hoje espera dois argumentos (`search` e `value`) — vale revisar essa chamada para manter a autenticação de gastos funcionando de ponta a ponta.
- `ExpansesDb.update` monta a query contra a tabela `users` em vez de `expanses` — revisar antes de usar em produção.
- Não há testes automatizados no repositório.
- O `role` de novos usuários é sempre fixado como `"user"`; não há rota para promover/alterar papéis.
- Sem expiração/rotação configurável fora do valor fixo de 3 dias para o access token.

---

## 👤 Autor

Desenvolvido por **[BrayanDevZN](https://github.com/BrayanDevZN)**.