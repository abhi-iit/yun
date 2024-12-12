from flask import Flask, request, jsonify
from datetime import datetime
from functools import wraps
import json

app = Flask(__name__)

# install pip using flask

# Decorator for validating date format
def validate_date_format(date_format="%d-%m-%Y"):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            date_str = request.args.get('start_date') or request.args.get('end_date')
            if date_str:
                try:
                    # Validate the date format
                    datetime.strptime(date_str, date_format)
                except ValueError:
                    return jsonify({"error": f"Invalid date format. Expected {date_format}."}), 422
            json_data = request.get_json()
            if json_data:
                date_str = json_data.get("date")
                if date_str:
                    try:
                        datetime.strptime(date_str, date_format)
                    except ValueError:
                        return jsonify({"error": f"Invalid date format. Expected {date_format}."}), 422
            return f(*args, **kwargs)
        return wrapped
    return decorator


# Decorator for validating basic authentication
def authenticate(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != 'user' or auth.password != 'password':
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapped


# Endpoint with validation and authentication
@app.route('/api/clients/<client_id>', methods=['POST'])
@authenticate
@validate_date_format(date_format="%d-%m-%Y")
def process_data(client_id):
    try:
        # Parse the JSON data
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No JSON payload provided"}), 422

        date = json_data.get("date")
        amount = json_data.get("amount")

        # Validate the JSON data types
        if not isinstance(date, str):
            return jsonify({"error": "'date' must be a string."}), 422
        if not isinstance(amount, (int, float)):
            return jsonify({"error": "'amount' must be a number."}), 422

        # Logic to process the data
        # For the sake of example, return the received data
        return jsonify({
            "client_id": client_id,
            "date": date,
            "amount": amount,
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__yun__':
    app.run(debug=True)