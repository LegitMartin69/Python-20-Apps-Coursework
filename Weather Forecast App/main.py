import streamlit as st
import plotly.express as px
from backend import get_data

# Add title, text input, slider, selectbox and subheader
st.title("Weather Forecast for the Next Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view", ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")

# checks if text input is not empty
if place:
    # Get the temperature/sky data
    try:
        filtered_data = get_data(place, days)

        if option == "Temperature":
            # Create a temperature plot
            temperatures = [dict["main"]["temp"] for dict in filtered_data]

            # Gives the temperature the correct format
            dates = [dict["dt_txt"] for dict in filtered_data]

            # Draws the graph
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date",
                                                              "y": "Temperature (Celsius)"})
            st.plotly_chart(figure)

        elif option == "Sky":
            # loads images
            images = {"Clear": "images/clear.png",
                      "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png",
                      "Snow": "images/snow.png"}
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]

            # matches images to the data from the API
            image_paths = [images[condition] for condition in sky_conditions]
            print(image_paths)
            st.write("Each line equals to one day, each image represents a 3 hour window")
            st.image(image_paths, width=80)
    except KeyError:
        st.write("That place does not exist")