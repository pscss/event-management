DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'keycloak') THEN
        CREATE DATABASE keycloak;
        RAISE NOTICE 'Keycloak database created';
    END IF;
END
$$;

DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'keycloak') THEN
        CREATE USER keycloak WITH PASSWORD 'keycloak';
        RAISE NOTICE 'Keycloak user created';
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;
