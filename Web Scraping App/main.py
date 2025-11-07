import re
import time
import requests
import selectorlib
import smtplib, ssl
import os
from email.message import EmailMessage

global URL
URL = "http://programmer100.pythonanywhere.com/tours/"

def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    print("DEBUG: Source scraped, returning...")
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    # Extracts the value from the returned dictionary with the key "tours"
    value = extractor.extract(source)["tours"]
    print("DEBUG: Value extracted, returning...")
    return value


def send_email(message):
    # Looks through the .env file, finds the first match for data labeled as APP_PASSWORD and email_address
    with open(".env", "r") as env:
        env_data = env.read()
        email_pattern = re.compile("EMAIL_ADDRESS[^a-zA-Z0-9]*([a-zA-Z0-9@.]+)\n")
        password_pattern = re.compile("APP_PASSWORD[^a-zA-Z0-9]*([a-zA-Z ]+)\n")
        gmail_app_password = re.findall(password_pattern, env_data)[0]
        email_address = re.findall(email_pattern, env_data)[0]
        gmail_app_password.strip()
        email_address.strip()

    # Assigns server-related variables
    host = "smtp.gmail.com"
    port = 465
    receiver = email_address
    context = ssl.create_default_context()

    # Set the contents of the email message
    email_message = EmailMessage()
    email_message["Subject"] = "New Event Found!"
    email_message.set_content(message)

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(email_address, gmail_app_password)
        server.sendmail(email_address, receiver, email_message.as_string())
    print("DEBUG: Email sent!")


def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")
    print("DEBUG: Data stored")


def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        content = read(extracted)
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(message=extracted)
        time.sleep(2)
