import cv2
import streamlit as st
import time

st.title("Simple web camera app")
start = st.button("Start the camera")

if start:
    
    streamlit_image = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        check, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        current_time = time.localtime()
        today = current_time.tm_wday
        match today:
            case 0:
                today = "Monday"
            case 1:
                today = "Tuesday"
            case 2:
                today = "Wednesday"
            case 3:
                today = "Thursday"
            case 4:
                today = "Friday"
            case 5:
                today = "Saturday"
            case 6:
                today = "Sunday"
        # print(f"{today}\n{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}")
        
        cv2.putText(img=frame, text=f"{today} {current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
                    org=(50,50), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(20, 100, 200),
                    thickness=2, lineType=cv2.LINE_AA)

        streamlit_image.image(frame)
