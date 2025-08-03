from flask import Flask, request, jsonify, render_template
from db_ops import insert_payment_attempt
import requests
from db_ops import insert_payment_attempt, get_failed_payments

app = Flask(__name__)



# Endpoint for processing  a payment
@app.route('/api/process-payment', methods=['POST'])
def process_payment():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()

    # Define the mock external API URL
    # Reqres.in is a good public service for this
    external_api_url = "https://jsonplaceholder.typicode.com/posts"


    # These are the fields we need to send to the external API
    # transform the data here to match the external API's format
    external_payload = {
        "title": "Payment from Project",
        "body": f"Amount: {data.get('amount')}, Card: {data.get('card_number_last_4')}",
        "userId": 1
    }

    try:
        response = requests.post(external_api_url, json=external_payload, timeout=10)

        payment_status = "SUCCESS" if response.status_code in [200, 201] else "FAILED"
        error_message = None if payment_status == "SUCCESS" else f"API returned status code: {response.status_code}"

        # Prepare the full data payload to be logged
        log_data = {
            'amount': data.get('amount'),
            'currency': data.get('currency'),
            'card_number_last_4': data.get('card_number_last_4'),
            'gateway_endpoint': external_api_url,
            'request_payload': external_payload,
            'response_status_code': response.status_code,
            'response_payload': response.json(),
            'payment_status': payment_status,
            'error_message': error_message
        }

        insert_payment_attempt(log_data)

        if payment_status == "SUCCESS":
            return jsonify({"message": "Payment processed successfully"}), 200
        else:
            return jsonify({"error": "Payment processing failed"}), 500
        
    except requests.exceptions.RequestException as e:
        # Handel network or timeout errors
        print(f"Network Error: {e}")
        log_data = {
            'amount': data.get('amount'),
            'currency': data.get('currency'),
            'card_number_last_4': data.get('card_number_last_4'),
            'gateway_endpoint': external_api_url,
            'request_payload': external_payload,
            'response_status_code': 0, # non-standard code for a network error
            'response_payload': {'error': str(e)},
            'payment_status': 'ERROR',
            'error_message': f"Network or timeout error: {e}"

        }
        insert_payment_attempt(log_data)
        return jsonify({"error":"Failed to connect to external API"}), 500

@app.route('/')
def homepage():
    return render_template('index.html')

# API endpoint for logging a payment
@app.route('/api/log_payment', methods=['POST'])
def log_payment():
    # Make sure the request contains JSON data
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 200
    

    data = request.get_json()

    # Basic validation here to check for required fields
    required_fields = ['amount', 'currency', 'card_number_last_4', 'gateway_endpoint', 'response_status_code', 'payment_status']
    if not all (field in data for field in required_fields):
        return jsonify({"error": "MIssing required fields"}), 400
    
    try:
        # Call the function to insert the data into the database
        insert_payment_attempt(data)
        return jsonify({"message": "Payment logged successfully"}), 201
    except Exception as e:
        # Log the error for troubleshooting
        print(f"Failed to log payment: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/api/payments/failed', methods=['GET'])
def failed_payments():
    try:
        failed_data = get_failed_payments()
        return jsonify(failed_data), 200
    except Exception as e:
        print(f"Failed to retrieve failed payments: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == '__main__':
    app.run(debug=True)