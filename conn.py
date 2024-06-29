import asyncpg


def create_connection():
    # Connection parameters
    connection_string = "postgresql+asyncpg://postgres:postgres@localhost:5433/postgres"

    try:
        # Create a new database session and return a new connection object
        connection = asyncpg.connect(connection_string)
        print("Connection to PostgreSQL DB successful")

        # Close the connection
        connection.close()
        print("Connection closed")

    except Exception as e:
        print(f"The error '{str(e)}' occurred")


if __name__ == "__main__":
    create_connection()
