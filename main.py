from flask import Flask, render_template

# Initialize Flask app
app = Flask("__name__")


# Define route for home page
@app.route("/")
def home():
    return render_template("home.html")


# Define route for API endpoint
@app.route("/api/v1/<station>/<date>")
def about(station, date):
    temperature = 23  # Dummy temperature value

    # Return JSON data with station, date, and temperature
    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }


if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True)
