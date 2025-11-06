import glob
import os
import cv2
import time
from emailing import send_email
from threading import Thread

video = cv2.VideoCapture(0)

first_frame = None
status_list = []
count = 1

def clean_folder():
    """
    Cleans the \images folder
    :return: None
    """
    print("clean folder function started")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("clean folder function ended")

while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame, 40, 255, cv2.THRESH_BINARY)[1]

    dill_frame = cv2.dilate(thresh_frame, None, iterations=2)

    countours, check = cv2.findContours(dill_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in countours:
        if cv2.contourArea(c) < 7500:
            continue
        x, y, w, h = cv2.boundingRect(c)
        rectangle = cv2.rectangle(frame, (x, y), (y + w, w + h), (0, 255, 0))
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/0{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            print("index: ", index)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True

        email_thread.start()

    cv2.imshow("MY VIDEO", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break


video.release()

clean_thread = Thread(target=clean_folder())
clean_thread.daemon = True

clean_thread.start()
