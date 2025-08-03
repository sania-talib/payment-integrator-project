import mysql.connector
from datetime import datetime
import json


db_config = {
    'host': '127.0.0.1',
    'user': 'payment_user',
    'password': 'password123',
    'database': 'payment_integrator'
}


def insert_payment_attempt(data):
    """Insert a new payment attempt record into the database"""

    conn = None

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        #The SQL INSERT statement
        sql = '''
            INSERT INTO payment_attempts (
            request_timestamp, amount, currency, card_number_last_4,
            gateway_endpoint, request_payload, response_status_code,
            response_payload, payment_status, error_message
            ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        '''

        # Prepare the data tuple
        values = (
            datetime.now().strftime('%y-%m-%d %H:%M:%S'),
            data['amount'],
            data['currency'],
            data['card_number_last_4'],
            data['gateway_endpoint'],
            json.dumps(data['request_payload']),
            data['response_status_code'],
            json.dumps(data['response_payload']),
            data['payment_status'],
            data.get('error_message')
            
        )

        cursor.execute(sql, values)
        conn.commit()
        print("Record inserted successfully!")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        if conn:
            conn.rollback()

    finally: 
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def get_failed_payments():
    """Retrives all payment attempts with a 'FAILED' or  'ERROR' status."""
    conn = None
    results = []
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True) # dictionary=True is great for returning JSON-like results

        # SQL  query to find all failed or error transactions
        sql = '''
            SELECT * FROM payment_attempts
            WHERE payment_status = 'FAILED' OR payment_status = 'ERROR'
            ORDER BY request_timestamp DESC
        '''

        cursor.execute(sql)
        results =  cursor.fetchall()
        print(f"Retrieved {len(results)} failed payments.")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# FOE TESTING PURPOSE ONLY

if __name__ == '__main__':
    mock_data = {
        'amount': 100.70,
        'currency': 'USD',
        'card_number_last_4': '1234',
        'gateway_endpoint': '/mock/payment',
        'request_payload': {'card_number': '1234', 'amount': 100.70},
        'response_status_code': 200,
        'response_payload': {'message': 'Success', 'transaction_id': 'xyz123'},
        'payment_status': 'SUCCESS'
    }
    insert_payment_attempt(mock_data)


    print("\n ----- Testing Failed Payments Retrival ----")
    failed_payments = get_failed_payments()
    if failed_payments:
        for payment in failed_payments:
            print(payment)
        else:
            print("No failed payments found")