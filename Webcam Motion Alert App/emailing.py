import smtplib
import imghdr
import regex
import re
from email.message import EmailMessage



# VPN might cause issues, please turn it off.

def send_email(image_path):
    """
    Sends an email via gmail, requires a functional EMAIL ADDRESS
    as well as a gmail APP PASSWORD
    It gets these from a local .env, which you might need to set up

    :param image_path: str, file path to the image that gets send
    :return: None
    """

    print("send email function started")

    # Looks through the .env file, finds the first match for data labeled as APP_PASSWORD and EMAIL_ADDRESS
    with open(".env", "r") as env:
        email_pattern = re.compile("EMAIL_ADDRESS[^a-zA-Z0-9]*([a-zA-Z0-9@.]+)\n")
        password_pattern = re.compile("APP_PASSWORD[^a-zA-Z0-9]*([a-zA-Z0-9@.]+)\n")
        GMAIL_APP_PASSWORD = re.findall(password_pattern, env.read())
        EMAIL_ADDRESS = re.findall(email_pattern, env.read())[0]

    # Sets up the email content
    email_message = EmailMessage()
    email_message["Subject"] = "Something is on the camera..."
    email_message.set_content("The camera saw something, look at the attachment")
    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    # Establishes connection with gmail servers, sends email and ends connections
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(EMAIL_ADDRESS, GMAIL_APP_PASSWORD)

    # SENDER and RECEIVER are the same email address
    gmail.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, email_message.as_string())
    gmail.quit()

    print("send email function ended")

if __name__ == "__main__":
    send_email(image_path="images/test.png")
