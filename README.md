# Revive

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
