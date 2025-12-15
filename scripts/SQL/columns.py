
import sqlite3

def add_column_if_not_exists(db_path, table_name, column_name, column_definition):
    connection = None
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # Check if the column exists using PRAGMA table_info
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [row for row in cursor.fetchall()]  # Extract column names
        
        if column_name not in columns:
            # Add the column if it does not exist
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_definition};")
            connection.commit()
            print(f"Column '{column_name}' added to '{table_name}'.")
        else:
            print(f"Column '{column_name}' already exists in '{table_name}'. Skipping.")
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()

# Usage example
# add_column_if_not_exists(
#     db_path="mydatabase.db",
#     table_name="users",
#     column_name="created_at",
#     column_definition="DATETIME DEFAULT CURRENT_TIMESTAMP"
# )   