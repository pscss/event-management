-- Create keycloak database if it doesn't exist
SELECT 'CREATE DATABASE keycloak' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'keycloak')\gexec

-- Create test_db database if it doesn't exist
SELECT 'CREATE DATABASE test_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'test_db')\gexec

-- Connect to keycloak database and grant privileges
\c keycloak
GRANT ALL PRIVILEGES ON DATABASE keycloak TO postgres;

-- Connect to test_db database and grant privileges
\c test_db
GRANT ALL PRIVILEGES ON DATABASE test_db TO postgres;
