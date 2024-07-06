#!/bin/bash
set -e

# Run the original entrypoint script of the postgres image
/usr/local/bin/docker-entrypoint.sh postgres &

# Wait for PostgreSQL to start
until pg_isready -U "$POSTGRES_USER"; do
  sleep 1
done

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'keycloak') THEN
            CREATE DATABASE keycloak;
            RAISE NOTICE 'Keycloak database created';
        END IF;
    END
    \$\$;

    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'keycloak') THEN
            CREATE USER keycloak WITH PASSWORD 'keycloak';
            RAISE NOTICE 'Keycloak user created';
        END IF;
    END
    \$\$;

    GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;
EOSQL
