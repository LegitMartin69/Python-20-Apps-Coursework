This repo contains projects made during "Python Mega Course: Build 20 Real-World Apps and AI Agents"

1. AI Chatbot (Chat with Einstein)
   - Uses Gradio + Google Gemini API
   - You can chat with Einstein, he answers with humor and personal stories
   - To run:
       - put your GEMINI_API_KEY in a .env file
       - install gradio, langchain, langchain-google-genai, python-dotenv
       - run: python main.py

2. ToDo Web App
   - Uses Streamlit
   - Simple to-do list that saves tasks in todo.txt
   - To run:
       - install streamlit
       -
       - run: streamlit run Web2.py
         
3. Weather Data API
   - Uses Flask + Pandas
   - Serves historical temperature data from weather stations
   - Endpoints: 
       - / → list of stations
       - /api/v1/<station>/<date> → temperature on a specific date
       - /api/v1/<station> → all data for a station
       - /api/v1/yearly/<station>/<year> → yearly data

   - To run:
       - install flask, pandas
       - run: python main.py
    
4. Weather Forecast Web App
    - Uses Streamlit + Plotly + OpenWeatherMap API
    - Shows weather forecast (temperature graph or sky images) for 1–5 days in a chosen city
    - To run:
       - get a free API key from openweathermap.org
       - put it in a .env file
       - install streamlit, plotly, requests
     
5. Diary Mood & Text Analysis App  
    - Uses Streamlit + Plotly + NLTK + Regex  
    - Combines two text analysis tools:  
        - Diary Mood Analyzer: reads diary entries, detects their positivity and negativity using NLTK’s Sentiment Intensity Analyzer, and visualizes results as line graphs over time  
        - Book Text Analyzer: allows searching through books for specific words, chapter titles, or sentences containing given words using regular expressions
    - To run Diary Mood Analyzer:  
        - install streamlit, plotly, nltk  
        - run: streamlit run main.py  
    - To run Book Text Analyzer:  
        - choose your text file (book) path in the script  
        - run: python exercise.py  

6. Motion Detection Security App  
    - Uses OpenCV + Threading + SMTP  
    - Monitors webcam feed, detects motion, saves frames, and emails an alert with the captured image  
    - To run:  
        - create a .env file with:
             - EMAIL_ADDRESS - the address to send the notification from, as well as to.
             - APP_PASSWORD - an app password generated from the gmail security menu.
        - install the required packages
        - run: python main.py  
        - press Q to quit
     
7. Event Tracker & Email Notifier  
   - Uses Requests + Selectorlib + SQLite + SMTP
   - Scrapes upcoming tour events from a webpage, stores the new ones in a local database, and sends an email notification when a new event appears.  
     Prevents duplicates by checking existing records.  
   - To run:  
       - Create a .env file with:  
           - EMAIL_ADDRESS – your Gmail address  
           - APP_PASSWORD – Gmail app password  
       - Install the required packages
       - Run:  
           python main.py

     
More projects to come!
