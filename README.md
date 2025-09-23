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


More projects to come!
