import mysql.connector

db_config = {
    'host': '127.0.0.1',
    'user': 'payment_user',
    'password': 'password123',
    'database': 'payment_integrator'
}

conn = None

try:
    #Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()


    #The SQL command to create the table is almost identical!
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payment_attempts(
            id INT AUTO_INCREMENT PRIMARY KEY,
            request_timestamp VARCHAR(255) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            currency VARCHAR(10) NOT NULL,
            card_number_last_4 VARCHAR(4) NOT NULL ,
            gateway_endpoint VARCHAR(255) NOT NULL,
            request_payload JSON NOT NULL,
            response_status_code INT NOT NULL,
            response_payload JSON NOT NULL,
            payment_status VARCHAR(50) NOT NULL,
            error_message TEXT             
         )

    ''')

    conn.commit()
    print("MySQL database and table 'payment_attempts' created successfully!")

except mysql.connector.Error as err:
    print(f"ERROR: {err}")

finally: 
    if conn:
        cursor.close()
        conn.close()