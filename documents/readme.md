# 💰 Control Expenses API

API REST para controle de gastos pessoais, com autenticação de usuários via **JWT** (armazenado em cookie `httpOnly`), senhas protegidas com **bcrypt** e persistência em **PostgreSQL**. O projeto segue uma arquitetura em camadas, separando claramente rotas, regras de negócio, validação e acesso a dados.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT"/>
  <img src="https://img.shields.io/badge/Bcrypt-8A2BE2?style=for-the-badge" alt="Bcrypt"/>
  <img src="https://img.shields.io/badge/Uvicorn-2A2A2A?style=for-the-badge" alt="Uvicorn"/>
</p>

---

## 📑 Índice

- [Sobre o projeto](#-sobre-o-projeto)
- [Arquitetura](#-arquitetura)
- [Estrutura de pastas](#-estrutura-de-pastas)
- [Tecnologias](#-tecnologias)
- [Como funciona a autenticação](#-como-funciona-a-autenticação)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração](#%EF%B8%8F-configuração)
- [Como executar](#-como-executar)
- [Rotas da API](#-rotas-da-api)
  - [Users](#-users-users)
  - [Expanses](#-expanses-expanses)
- [Modelo de dados](#-modelo-de-dados)
- [Logs](#-logs)
- [Roadmap / melhorias conhecidas](#-roadmap--melhorias-conhecidas)

---

## 📌 Sobre o projeto

O **Control Expenses** é uma API construída em **FastAPI** para que cada usuário cadastre, consulte, atualize e remova seus próprios gastos (nome, quantidade e preço), com o total calculado automaticamente (`quantity * price`). Cada gasto pertence a um usuário autenticado — o vínculo é feito automaticamente pelo `user_id` extraído do token JWT presente no cookie da requisição.

---

## 🏗️ Arquitetura

O projeto segue uma **arquitetura em camadas**, inspirada em Clean Architecture, onde cada módulo tem uma responsabilidade única e depende apenas da camada abaixo dele:

```
Controller  → recebe a requisição HTTP, define rotas, middlewares e dependências
     ↓
Service     → camada de "montagem": une domain + repository + infra em instâncias prontas para uso
     ↓
Domain      → regras de negócio, validação de dados (Pydantic) e criptografia (JWT/hash)
     ↓
Repository  → acesso a dados, executa as queries SQL via SQLAlchemy
     ↓
Infra       → configuração (variáveis de ambiente), conexão com o banco e criação de tabelas
```

### Fluxo de uma requisição autenticada

```
Cliente
  │
  ▼
FastAPI (controller/main.py)
  │
  ├─► CORS Middleware (libera todas as origens)
  │
  ├─► Middleware de autenticação (controller/midllewares/users.py)
  │     └─ valida regras específicas da rota /users
  │        (usuário já existe? não existe? senha confere?)
  │
  ├─► Router (users ou expanses)
  │     └─ Depends(depends) → service/depends.py (GetUser)
  │           1. lê o cookie "user_token"
  │           2. decodifica o JWT
  │           3. busca o usuário no banco
  │           4. retorna o "id" interno do usuário (ou levanta HTTPException)
  │
  ├─► Domain (Pydantic models) valida o corpo da requisição
  │
  ├─► Repository executa o SQL via SQLAlchemy (engine criada em infra/)
  │
  ▼
PostgreSQL
```

### Responsabilidade de cada camada

| Camada | Pasta | Responsabilidade |
|---|---|---|
| **Controller** | `src/controller` | Define os `APIRouter` (rotas), o middleware de autenticação e a instância principal do FastAPI (`Main`). |
| **Service** | `src/service` | "Cola" as camadas — instancia `ControlDb`, `JwtToken`, `HashPass` e o `GetUser`, deixando prontos para uso nos controllers. |
| **Domain** | `src/domain` | Contém os *models* Pydantic (validação de entrada), as regras de negócio de usuário (`ValidUsers`) e as classes de criptografia (`JwtToken`, `HashPass`). |
| **Repository** | `src/repository` | Executa as queries SQL (raw SQL via `sqlalchemy.text`) para as tabelas `users` e `expanses`. |
| **Infra** | `src/infra` | Carrega variáveis de ambiente (`url`, `sing`), cria a `Engine` do SQLAlchemy e o schema do banco (`start_schema`). |
| **Logs** | `src/logs` | Configuração global de logging (arquivo `app.log` + `stdout`). |

---

## 📂 Estrutura de pastas

```
Control/
├── config/
│   ├── dockerfile              # imagem da API
│   ├── docker-compose.yml      # orquestração do container da API
│   └── requirements.txt        # dependências Python
│
└── src/
    ├── controller/
    │   ├── main.py              # cria e configura a instância FastAPI
    │   ├── dependences/
    │   │   └── depends.py       # dependência de autenticação usada nas rotas
    │   ├── midllewares/
    │   │   └── users.py         # middleware HTTP que valida regras da rota /users
    │   └── handles/
    │       ├── users.py         # rotas de usuário (/users)
    │       └── expanses.py      # rotas de gastos (/expanses)
    │
    ├── service/
    │   ├── manage.py             # agrega db, jwt, hash, midleware e depends
    │   ├── db.py                 # instancia o ControlDb com a engine
    │   ├── depends.py            # GetUser: extrai o usuário autenticado do token
    │   ├── encode.py             # instancia JwtToken e HashPass com a chave (sing)
    │   └── midleware.py          # ValidMidlleware: liga o middleware às regras de negócio
    │
    ├── domain/
    │   ├── module.py             # ponto único de importação dos módulos do domínio
    │   ├── models/
    │   │   ├── model_user.py     # validação Pydantic de usuário (senha, e-mail, login)
    │   │   └── model_expanses.py # validação Pydantic de gastos
    │   ├── role/
    │   │   └── users.py          # regra de negócio: usuário existe / não existe / senha válida
    │   └── encode/
    │       ├── jwt.py            # criação e leitura de tokens JWT
    │       └── hash.py           # hash e verificação de senha com bcrypt
    │
    ├── repository/
    │   ├── manage.py             # ControlDb: agrega UsersDb e ExpansesDb
    │   └── db/
    │       ├── users.py          # CRUD SQL da tabela users
    │       └── expanses.py       # CRUD SQL da tabela expanses
    │
    ├── infra/
    │   ├── manage.py             # cria a engine do banco / comando start_schema
    │   ├── core/
    │   │   ├── settings.py       # carrega variáveis de ambiente (.env)
    │   │   ├── security.py       # regras de rota protegidas por método/path
    │   │   └── .env              # variáveis de ambiente (não versionar em produção)
    │   └── database/
    │       ├── connection.py     # cria e testa a conexão (Engine) com o PostgreSQL
    │       └── tables.py         # cria as tabelas users e expanses caso não existam
    │
    └── logs/
        ├── log.py                # configuração do logger (arquivo + console)
        └── app.log                # arquivo de log gerado em runtime
```

---

## 🧰 Tecnologias

- **[Python 3.14](https://www.python.org/)**
- **[FastAPI](https://fastapi.tiangolo.com/)** — framework web assíncrono
- **[Uvicorn](https://www.uvicorn.org/)** — servidor ASGI
- **[SQLAlchemy (Core)](https://www.sqlalchemy.org/)** — execução das queries SQL e gerenciamento da engine
- **[PostgreSQL](https://www.postgresql.org/)** — banco de dados relacional (tabelas usam `serial`, `uuid`, `timestamptz`)
- **[Pydantic](https://docs.pydantic.dev/)** — validação de dados de entrada
- **[PyJWT](https://pyjwt.readthedocs.io/)** — geração e leitura de tokens JWT
- **[bcrypt](https://pypi.org/project/bcrypt/)** — hash seguro de senhas
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** — carregamento de variáveis de ambiente
- **[Docker](https://www.docker.com/)** — containerização da aplicação

> ⚠️ O arquivo `config/requirements.txt` incluído no repositório corresponde a um *pip freeze* do sistema (contém pacotes não relacionados ao projeto, como `Sphinx`, `PyGObject`, `dbus-python`) e **não reflete as dependências reais da aplicação**. Recomenda-se substituí-lo por um `requirements.txt` contendo apenas:
> ```
> fastapi
> uvicorn
> sqlalchemy
> psycopg2-binary
> pydantic
> pyjwt
> bcrypt
> python-dotenv
> ```

---

## 🔐 Como funciona a autenticação

1. No **cadastro** (`POST /users`) ou **login** (`GET /users`), a API gera um JWT contendo `public_id`, `name` e `role` do usuário e o envia como cookie `httpOnly` + `SameSite=Strict` chamado **`user_token`**.
2. Em rotas protegidas (como `/expanses`), a dependência `depends` (em `controller/dependences/depends.py`) lê esse cookie, decodifica o token e busca o usuário no banco, retornando o `id` interno para uso nas queries.
3. Um **middleware global** (`controller/midllewares/users.py`) intercepta especificamente requisições em `/users` e aplica regras de negócio antes mesmo de chegar na rota:
   - Bloqueia criação de usuário se o e-mail já existir.
   - Bloqueia atualização/exclusão se o usuário não existir.
   - Valida a senha informada contra o hash salvo no banco.
4. O **logout** (`DELETE /users/logout`) simplesmente remove o cookie `user_token`.

---

## ✅ Pré-requisitos

- Python 3.14+ (ou Docker)
- Uma instância PostgreSQL acessível
- Docker e Docker Compose (opcional, para rodar containerizado)

---

## ⚙️ Configuração

Crie o arquivo `src/infra/core/.env` com as seguintes variáveis:

```env
url=postgresql+psycopg2://usuario:senha@host:5432/nome_do_banco
sing=uma-chave-secreta-forte-para-assinar-o-jwt
```

| Variável | Descrição |
|---|---|
| `url` | String de conexão do SQLAlchemy com o PostgreSQL |
| `sing` | Chave secreta usada para assinar/validar os tokens JWT (algoritmo `HS256`) |

---

## 🚀 Como executar

### Opção 1 — Docker (recomendado)

```bash
git clone https://github.com/BrayanDevZN/Control_expenses.git
cd Control_expenses/Control
docker compose -f config/docker-compose.yml up --build
```

A API sobe em `http://localhost:8000`. O próprio container executa a criação das tabelas antes de iniciar o servidor:

```bash
python -m infra.manage start_schema && python -m uvicorn controller.main:app --host 0.0.0.0 --port 8000
```

### Opção 2 — Ambiente local

```bash
git clone https://github.com/BrayanDevZN/Control_expenses.git
cd Control_expenses/Control

# criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# instalar dependências (ver seção "Tecnologias")
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic pyjwt bcrypt python-dotenv

cd src

# criar as tabelas no banco
python -m infra.manage start_schema

# iniciar a API
python -m uvicorn controller.main:app --reload --port 8000
```

Documentação interativa gerada automaticamente pelo FastAPI:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🛣️ Rotas da API

### 👤 Users (`/users`)

| Método | Rota | Autenticação | Descrição |
|---|---|---|---|
| `POST` | `/users/` | Não | Cria uma nova conta e retorna o cookie `user_token` |
| `GET` | `/users/` | Não | Login — valida e-mail/senha e retorna o cookie `user_token` |
| `PATCH` | `/users/` | Cookie `user_token` | Atualiza a senha do usuário autenticado |
| `DELETE` | `/users/{password}` | Cookie `user_token` | Remove a conta do usuário autenticado |
| `DELETE` | `/users/logout` | Não | Remove o cookie `user_token` (logout) |

**Regras de validação de usuário** (`domain/models/model_user.py`):
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

**Resposta**: `200 OK` + cookie `user_token` definido.
</details>

<details>
<summary><strong>GET /users/</strong> — Login</summary>

**Body**
```json
{
  "email": "brayan@gmail.com",
  "password": "Senha123"
}
```

**Resposta**: `200 OK` + cookie `user_token` definido.
Em caso de credenciais inválidas: `401` (usuário não encontrado) ou `501` (senha inválida).
</details>

<details>
<summary><strong>PATCH /users/</strong> — Atualizar senha</summary>

Requer o cookie `user_token` já definido (usuário autenticado).

**Body**
```json
{
  "password": "NovaSenha123"
}
```
</details>

<details>
<summary><strong>DELETE /users/{password}</strong> — Excluir conta</summary>

Requer o cookie `user_token`. A senha atual é enviada como parâmetro de rota para confirmação.

```
DELETE /users/Senha123
```
</details>

<details>
<summary><strong>DELETE /users/logout</strong> — Logout</summary>

Remove o cookie de sessão. Não requer body.
</details>

---

### 💸 Expanses (`/expanses`)

Todas as rotas abaixo exigem o cookie `user_token` (usuário autenticado) — o `user_id` é resolvido automaticamente a partir do token.

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
| `role` | `text` | Papel do usuário (ex.: `admin`, `dev`, `user`) |
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

> As tabelas são criadas automaticamente ao rodar `python -m infra.manage start_schema` (comando já incluído no `CMD` do Dockerfile).

---

## 📝 Logs

Toda a aplicação usa um logger centralizado (`src/logs/log.py`) que grava simultaneamente:
- No console (`stdout`)
- No arquivo `src/logs/app.log`

Formato: `AAAA-MM-DD HH:MM:SS [NÍVEL] mensagem`

---

## 🔭 Roadmap / melhorias conhecidas

- Corrigir `config/requirements.txt` para refletir as dependências reais do projeto.
- Padronizar o retorno de erros da API (hoje a maioria das exceções é convertida genericamente em `501`).
- Adicionar testes automatizados (unitários e de integração).
- Adicionar refresh token / expiração configurável para o JWT.
- Adicionar variável de ambiente para configurar `allow_origins` do CORS em produção (atualmente `"*"`).

---

## 👤 Autor

Desenvolvido por **[BrayanDevZN](https://github.com/BrayanDevZN)**.