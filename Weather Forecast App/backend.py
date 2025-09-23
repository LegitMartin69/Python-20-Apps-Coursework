import requests

def get_data(place, forecast_days=5, type=None):
    """
    Gets the weather data through openweathermap.org api
    Gets the API_KEY from the .env file
    """

    API_KEY = ""
    with open(".env") as env:
        API_KEY = str(env.readline())
        API_KEY.strip()
    # print(API_KEY)
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"
    response = requests.get(url)
    content = response.json()

    nr_values = 8 * forecast_days
    filtered_data = content["list"][:nr_values]

    if type == "Temperature":
        filtered_data = [dict["main"]["temp"] for dict in filtered_data]
    elif type == "Sky":
        filtered_data = [dict["weather"][0]["main"] for dict in filtered_data]

    return filtered_data

if __name__ == "__main__":

    print(get_data(place="Tokyo", forecast_days=3, type="Temperature"))