import pymysql
import config

# Create database connection
def create_connection():
    connection = pymysql.connect(
        host=config.customhost,
        user=config.customuser,
        password=config.custompass,
        database=config.customdb
    )
    return connection

# Create employees table if it doesn't exist
def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        employee_id VARCHAR(255) NOT NULL UNIQUE,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        location VARCHAR(255) NOT NULL,
        image_url VARCHAR(500),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    cursor.execute(create_table_query)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_table()
    print("Table created successfully!")