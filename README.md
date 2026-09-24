# Products API 🚀

API RESTful moderna, rápida y escalable para la gestión de productos, construida con **FastAPI**, **SQLModel**, **Alembic**, y empaquetada con **Docker** y **uv**.

---

## 📋 Características

* **Framework:** FastAPI con tipado estricto y validaciones automáticas.
* **ORM:** SQLModel (fusión de SQLAlchemy y Pydantic).
* **Migraciones:** Alembic para control de versiones del esquema de base de datos.
* **Seguridad y Validación:** Validación de esquemas con Pydantic (`Field` para precios positivos y stock no negativo).
* **Paginación:** Parámetros `skip` y `limit` en el endpoint de listado.
* **Testing:** Suite completa de pruebas automatizadas con `pytest` y base de datos SQLite en memoria (aislada).
* **Contenedorización:** Listo para desplegar con `Dockerfile` y `docker-compose.yml`.
* **CORS:** Configurado para integración inmediata con frontends.

---

## 📁 Estructura del Proyecto

```text
products-api/
│
├── alembic/                 # Migraciones de base de datos
│   └── versions/            # Scripts de versión generados
├── app/
│   ├── exceptions/          # Excepciones personalizadas (404, 409, etc.)
│   ├── models/              # Modelos de base de datos (SQLModel table=True)
│   ├── routes/              # Endpoints HTTP (APIRouter)
│   ├── schemas/             # Esquemas de entrada y salida (DTOs de Pydantic)
│   ├── services/            # Lógica de negocio
│   ├── database.py          # Configuración de motor de base de datos y sesiones
│   └── main.py              # Punto de entrada de la aplicación FastAPI
├── tests/                   # Pruebas automatizadas (pytest)
│   ├── conftest.py          # Fixtures y SQLite en memoria
│   └── test_products.py     # Pruebas CRUD y validaciones
├── Dockerfile               # Configuración de imagen de Docker
├── docker-compose.yml       # Orquestación de contenedores
├── pyproject.toml           # Configuración de dependencias y proyecto
├── requirements.txt         # Dependencias para Docker
└── README.md
```

---

## 🛠️ Requisitos Previos

* Python 3.12+
* [uv](https://docs.astral.sh/uv/) (recomendado) o `pip`
* Docker y Docker Compose (opcional para ejecución en contenedores)

---

## 🚀 Inicio Rápido (Local)

### 1. Clonar el repositorio y configurar variables de entorno
Crea un archivo `.env` basado en `.env_example`:

```bash
cp .env_example .env
```

Configura tu cadena de conexión a PostgreSQL en `.env`:
```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
```

### 2. Instalar dependencias con `uv`
```bash
uv sync
```

### 3. Aplicar migraciones
```bash
uv run alembic upgrade head
```

### 4. Iniciar el servidor de desarrollo
```bash
uv run uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`.

---

## 🧪 Pruebas Automatizadas

El proyecto incluye tests con base de datos en memoria para no alterar la base de datos de producción:

```bash
uv run pytest
```

---

## 🐳 Ejecución con Docker

### Construir y levantar con Docker Compose
```bash
docker compose up --build -d
```

La API estará accesible en `http://localhost:8000`.

Para detener el contenedor:
```bash
docker compose down
```

---

## 📖 Documentación Interactiva

FastAPI genera documentación interactiva automáticamente:
* **Swagger UI:** `http://localhost:8000/docs`
* **ReDoc:** `http://localhost:8000/redoc`
