import re
import time
import requests
import selectorlib
import smtplib, ssl
import os
import sqlite3
from email.message import EmailMessage

global URL
URL = "http://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("database.db")


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
    # Splits the extracted string into 3 separate strings and cleans them of whitespaces
    row = extracted.split(",")
    row = [item.strip() for item in row]

    # Assigns a new cursor
    cursor = connection.cursor()
    # Inserts values into the Database
    cursor.execute("INSERT INTO Events VALUES(NULL, ?,?,?)", row)
    # Makes changes
    connection.commit()

    print("DEBUG: Data stored")


def read(extracted):
    # Splits the extracted string into 3 separate strings and cleans them of whitespaces
    row = extracted.split(",")
    row = [item.strip() for item in row]

    # Assigns a new cursor
    cursor = connection.cursor()

    # Selects the extracted text from Database and pastes it into "rows" variable
    cursor.execute("SELECT band,city,date_text FROM Events WHERE band=? AND city=? AND date_text=?", row)
    rows = cursor.fetchall()

    print("DEBUG: Data read, found: ", rows)
    return rows


def clear_database():
    """Deletes all the records from database Events"""
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Events")
    connection.commit()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = \"Events\"")
    connection.commit()
    print("DEBUG: Database cleared of all records")


def run_program(amount: int):
    entries_amount: int = 0
    while entries_amount < amount:
        # Scrapes and extracts data
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        # Checks if the extracted data have changed
        if extracted != "No upcoming tours":
            row = read(extracted)
            print(row)
            # Checks if the returned list from read() is not empty A.K.A. If the entry already exists.
            if not row:
                store(extracted)
                send_email(message=extracted)
            else:
                print("DEBUG: Data probably already exists")

            # Fetches all ids from the database
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM Events")
            ids = cursor.fetchall()
            # Converts the output to a list
            ids = list(ids)
            # Finds the last entry and turns it into an INT
            last_id = int(ids[-1][0])
            entries_amount = last_id

        time.sleep(1.5)

    print("The program has finished recording all existing events (2)")
    run_program_again = input("Would you like to run the program again? (YES/NO): ")
    run_program_again.lower()
    if run_program_again == "yes":
        clear_database()
        run_program(2)
    else:
        print("DEBUG: Ending program...")
        time.sleep(1.5)
        clear_database()
        pass

if __name__ == "__main__":
    run_program(2)
