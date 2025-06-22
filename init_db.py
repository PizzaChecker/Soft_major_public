import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'login_app/database.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema1.sql')

def init_db():
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(DATABASE_PATH)

        # Use a context manager to ensure the file is properly closed
        with open(SCHEMA_PATH, 'r') as f:
            connection.executescript(f.read())
        
        connection.commit()
        print("Database initialised successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}") #Change in future
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Ensure the connection is closed
        if connection:
            connection.close()

if __name__ == '__main__':
    init_db()