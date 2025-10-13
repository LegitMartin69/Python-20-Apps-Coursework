import re
from nltk.sentiment import SentimentIntensityAnalyzer
import glob
import streamlit as st
import plotly.express as px


analyzer = SentimentIntensityAnalyzer()

def find_polarity(file_path):
    """
    Scans a file and finds from its content whether its positive or negative

    :param file_path: path of the file to scan
    :return: Return a Dictionary with 3 keys - date, neg (negativity), pos (positivity)
    """
    # Opens a diary entry
    with open(file_path, "r", encoding="utf-8") as file:
        diary_entry = file.read()
        polarity = analyzer.polarity_scores(diary_entry)
        # Using Regex finds the date from the file path
        pattern = re.compile("diary\\\\([^.]+)")
        date = re.findall(pattern, file_path)[0]
        #print(date)
        return {'date': date, 'neg': polarity['neg'], 'pos': polarity['pos']}


# Scans for the diary files in the directory, from which this program was run.
file_path_list = glob.glob("*\\diary\\\\**?", recursive=True)

# Finds the polarity for each diary entry
polarity_list = []
for diary_name in file_path_list:
    polarity_list.append(find_polarity(diary_name))
    # print(polarity_list)
# print(polarity_list)

# Splits the polarity dictionary into three lists
# All lists are come from a sorted dictionary, use matching indexes in different lists to get matching info.
positive_pol = [i['pos'] for i in polarity_list]
negative_pol = [i['neg'] for i in polarity_list]
dates = [i['date'] for i in polarity_list]

# Website Elements
st.title("Diary Mood Analysis")
# Draw graphs
if positive_pol and negative_pol and dates != []:
    # Positivity graph
    st.subheader("Positivity")
    pos_figure = px.line(x=dates, y=positive_pol, labels={"x": "Date", "y": "Positivity"})
    st.plotly_chart(pos_figure)
    # Negativity graph
    st.subheader("Negativity")
    neg_figure = px.line(x=dates, y=negative_pol, labels={"x": "Date", "y": "Negativity"})
    st.plotly_chart(neg_figure)
