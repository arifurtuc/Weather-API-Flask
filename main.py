from flask import Flask, render_template
import pandas as pd

# Initialize Flask app
app = Flask("__name__")


# Define route for home page
@app.route("/")
def home():
    return render_template("home.html")


# Define route for API endpoint
@app.route("/api/v1/<station>/<date>")
def fetch_data(station, date):
    # Extract temperature data for the given station and date
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10

    # Return JSON data with station, date, and temperature
    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }


if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True)
