# Revive

## Frontend

Build and start the React frontend with Docker Compose:

```sh
docker compose up --build frontend
```

The frontend is available at `http://localhost:5173`.

## Backend

Start the FastAPI backend with Docker Compose:

```sh
docker compose up --build backend
```

The API is available at `http://localhost:8000` and its health endpoint is
`http://localhost:8000/health`.

For local development, install the backend dependencies and run:

```sh
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## PostgreSQL

Copy `.env.example` to `.env` and adjust the values if needed, then start PostgreSQL:

```sh
docker compose up -d
```

The database is available on `localhost:5432`. Stop the service with:

```sh
docker compose down
```

Data is stored in the `postgres_data` Docker volume and is preserved when the service is stopped.

## Database migrations

Flyway migrations are stored in `database/migrations/` and use this naming format:

```text
V1__initial_schema.sql
V2__add_user_name.sql
V3__add_indexes.sql
```

Start the database, then apply pending migrations:

```sh
docker compose up -d database
docker compose --profile migration run --rm migrate
```

Check migration status without applying changes:

```sh
docker compose --profile migration run --rm migrate info
```

For every schema change, add a new migration file. Do not edit a migration that has already been applied. Flyway records applied migrations in `flyway_schema_history` and skips them on later runs.

To test all migrations from an empty database during local development, this deletes local database data:

```sh
docker compose down -v
docker compose up -d database
docker compose --profile migration run --rm migrate
```
