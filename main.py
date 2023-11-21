from flask import Flask, render_template
import pandas as pd

# Initialize Flask app
app = Flask("__name__")


# Define route for home page
@app.route("/")
def home():
    """
    Renders the home page with station data.

    Reads station data from a CSV file, extracts station ID and name,
    and renders the 'home.html' template using the extracted data.
    """
    stations = pd.read_csv("data_small/stations.txt", skiprows=17)
    stations = stations[["STAID", "STANAME                                 "]]
    return render_template("home.html", data=stations.to_html())


# Define route for API endpoint
@app.route("/api/v1/<station>/<date>")
def fetch_data(station, date):
    """
    Retrieves temperature data for a specific weather station on a given date.

    :param station: The station ID.
    :param date: The date for which temperature data is requested.
    :return: JSON containing station ID, date, and temperature information.
    """
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }


@app.route("/api/v1/<station>")
def all_data(station):
    """
    Retrieves all data for a specific weather station.

    :param station: The station ID.
    :return: JSON containing all data for the given station.
    """
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    """
    Retrieves yearly data for a specific weather station for the given year.

    :param station: The station ID.
    :param year: The year for which data is requested.
    :return: JSON containing yearly data for the given station and year.
    """
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))]
    result = result.to_dict(orient="records")
    return result


if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True)
