from flask import Flask, render_template_string, request

app = Flask(__name__)

# Vehicle base fare and mileage (simplified)
VEHICLES = {
    "auto": {"base_fare": 25, "km_rate": 10},
    "cab": {"base_fare": 50, "km_rate": 15},
    "taxi": {"base_fare": 60, "km_rate": 20}
}

# Assumed current fuel price and inflation in India
FUEL_COST_PER_KM = 10    # ₹ per km
INFLATION_RATE = 7       # % average annual

html_page = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Meter India</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
        input, select { padding: 5px; margin: 5px; }
        button { padding: 10px 20px; margin: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>AI Meter India</h1>
    <form method="POST">
        <label>Name:</label>
        <input type="text" name="name" required><br><br>
        <label>Vehicle Type:</label>
        <select name="vehicle" required>
            <option value="auto">Auto</option>
            <option value="cab">Cab</option>
            <option value="taxi">Taxi</option>
        </select><br><br>
        <label>Distance (km):</label>
        <input type="number" name="distance" step="0.1" required><br><br>
        <button type="submit">Calculate Fare</button>
    </form>

    {% if fare %}
    <h2>Hello {{ name }}!</h2>
    <h2>Estimated Fare for {{ vehicle }}: ₹{{ fare }}</h2>
    {% endif %}
</body>
</html>
"""

def calculate_fare(vehicle, distance):
    data = VEHICLES.get(vehicle)
    if not data:
        return 0
    base = data["base_fare"]
    km_rate = data["km_rate"]
    fare = base + distance * km_rate * (1 + INFLATION_RATE / 100)
    return round(fare, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    fare = None
    name = ""
    vehicle = ""
    if request.method == 'POST':
        name = request.form['name']
        vehicle = request.form['vehicle']
        distance = float(request.form['distance'])
        fare = calculate_fare(vehicle, distance)
    return render_template_string(html_page, fare=fare, name=name, vehicle=vehicle)

if __name__ == '__main__':
    app.run(debug=True)
