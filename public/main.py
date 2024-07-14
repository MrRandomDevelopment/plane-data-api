from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# In-memory storage for flights
flights_active = []

# Fetch all active flights
@app.route('/fetch', methods=['GET'])
def fetch():
    return jsonify(flights_active), 200

# Add a new flight
@app.route('/new', methods=['POST', 'GET'])
def new():
    if request.method == 'POST':
        data = request.get_json()  # Read JSON data from request body
    else:
        data = request.args.to_dict()  # Read data from query parameters

    print("Received data:", data)  # Debugging line to print received data
    required_keys = ['RobloxUsername', 'Squawk', 'lat', 'lon', 'livery', 'altitude', 'speed', 'Heading', 'AircraftType']
    if not all(key in data for key in required_keys):
        missing_keys = [key for key in required_keys if key not in data]
        print("Missing keys:", missing_keys)  # Debugging line to print missing keys
        return jsonify({"error": "Missing data", "missing_keys": missing_keys}), 400
    flights_active.append(data)
    return jsonify({"message": "Flight added"}), 201

# Update an existing flight
@app.route('/update', methods=['PUT', 'GET'])
def update():
    if request.method == 'PUT':
        data = request.get_json()  # Read JSON data from request body
    else:
        data = request.args.to_dict()  # Read data from query parameters

    if 'RobloxUsername' not in data:
        return jsonify({"error": "Missing RobloxUsername"}), 400
    for flight in flights_active:
        if flight['RobloxUsername'] == data['RobloxUsername']:
            flight.update({key: data[key] for key in data if key != 'RobloxUsername'})
            return jsonify({"message": "Flight updated"}), 200
    return jsonify({"error": "Flight not found"}), 404

# Remove a flight
@app.route('/remove', methods=['DELETE', 'GET'])
def remove():
    if request.method == 'DELETE':
        data = request.get_json()  # Read JSON data from request body
    else:
        data = request.args.to_dict()  # Read data from query parameters

    if 'RobloxUsername' not in data:
        return jsonify({"error": "Missing RobloxUsername"}), 400
    global flights_active
    flights_active = [flight for flight in flights_active if flight['RobloxUsername'] != data['RobloxUsername']]
    return jsonify({"message": "Flight removed"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
