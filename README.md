# SkyLox Flight API

This guide will help you set up the SkyLox Flight API using Flask. This API allows you to manage active flights with functionalities to fetch, add, update, and remove flights.

## Prerequisites

1. **Python**: Make sure you have Python installed.
2. **Flask**: Install Flask and Flask-CORS.
   ```bash
   pip install Flask Flask-CORS
   ```

## Step-by-Step Setup

### 1. Create the Flask Application

Create a Python file (e.g., `main.py`) with the following content:

```python
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
```

### 2. Running the Application

Run the Flask application:

```bash
python main.py
```

The server will start and listen on `0.0.0.0:8080`.

## API Endpoints

### Fetch All Active Flights

**Endpoint**: `/fetch`

**Method**: `GET`

**Description**: Fetches all active flights.

**Response**:
```json
[
  {
    "RobloxUsername": "example_user",
    "Squawk": "1234",
    "lat": "40.7128",
    "lon": "-74.0060",
    "livery": "default",
    "altitude": "30000",
    "speed": "500",
    "Heading": "90",
    "AircraftType": "A320"
  }
]
```

### Add a New Flight

**Endpoint**: `/new`

**Method**: `POST` or `GET`

**Description**: Adds a new flight.

**Request Body**:
```json
{
  "RobloxUsername": "example_user",
  "Squawk": "1234",
  "lat": "40.7128",
  "lon": "-74.0060",
  "livery": "default",
  "altitude": "30000",
  "speed": "500",
  "Heading": "90",
  "AircraftType": "A320"
}
```

**Response**:
```json
{
  "message": "Flight added"
}
```

### Update an Existing Flight

**Endpoint**: `/update`

**Method**: `PUT` or `GET`

**Description**: Updates an existing flight.

**Request Body**:
```json
{
  "RobloxUsername": "example_user",
  "Squawk": "4321",
  "lat": "40.7128",
  "lon": "-74.0060",
  "livery": "new_livery",
  "altitude": "35000",
  "speed": "550",
  "Heading": "180",
  "AircraftType": "A320"
}
```

**Response**:
```json
{
  "message": "Flight updated"
}
```

### Remove a Flight

**Endpoint**: `/remove`

**Method**: `DELETE` or `GET`

**Description**: Removes a flight.

**Request Body**:
```json
{
  "RobloxUsername": "example_user"
}
```

**Response**:
```json
{
  "message": "Flight removed"
}
```

## Sending Data via HTML Form

You can use an HTML form to send data to the API. Create an HTML file (e.g., `index.html`) with the following content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Flight Management</title>
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        margin: 0;
        padding: 20px;
    }
    .container {
        max-width: 600px;
        margin: 0 auto;
        background: #fff;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    h2 {
        margin-top: 0;
    }
    input[type="text"], input[type="number"] {
        width: calc(100% - 22px);
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #ddd;
    }
    button {
        padding: 10px 20px;
        background: #007bff;
        color: #fff;
        border: none;
        cursor: pointer;
    }
    button:hover {
        background: #0056b3;
    }
    .message {
        margin: 10px 0;
        padding: 10px;
        border: 1px solid #ddd;
        background: #f9f9f9;
    }
</style>
</head>
<body>
<div class="container">
<h2>Add or Update Flight</h2>
<form id="flightForm">
<input type="text" id="RobloxUsername" name="RobloxUsername" placeholder="Roblox Username" required>
<input type="text" id="Squawk" name="Squawk" placeholder="Squawk" required>
<input type="number" step="any" id="lat" name="lat" placeholder="Latitude" required>
<input type="number" step="any" id="lon" name="lon" placeholder="Longitude" required>
<input type="text" id="livery" name="livery" placeholder="Livery" required>
<input type="number" id="altitude" name="altitude" placeholder="Altitude" required>
<input type="number" id="speed" name="speed" placeholder="Speed" required>
<input type="number" id="Heading" name="Heading" placeholder="Heading" required>
<input type="text" id="AircraftType" name="AircraftType" placeholder="Aircraft Type" required>
<button type="button" onclick="submitForm()">Submit</button>
</form>
<div class="message" id="message"></div>
</div>
<script>
    async function submitForm() {
        const form = document.getElementById('flightForm');
        const formData = new FormData(form);

        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        const url = `https://example.com:8080/new`;

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
           

 if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const result = await response.json();
            const message = document.getElementById('message');
            if (result.error) {
                message.textContent = `Error: ${result.error}`;
            } else {
                message.textContent = result.message;
            }
        } catch (error) {
            const message = document.getElementById('message');
            message.textContent = `Error: ${error.message}`;
        }
    }
</script>
</body>
</html>
```

### Sending Data via URL

You can also send data directly through the browser by navigating to a URL with query parameters. For example:

```
https://example.com/new?RobloxUsername=example_user&Squawk=1234&lat=40.7128&lon=-74.0060&livery=default&altitude=30000&speed=500&Heading=90&AircraftType=A320
```

This URL sends a new flight with the specified parameters to the `/new` endpoint. You can do the same with the `/update` and `/remove` endpoints.
