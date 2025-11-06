import smtplib
import imghdr
from email.message import EmailMessage

# VPN might cause issues, please turn it off.

def send_email(image_path):
    """
    Sends an email via gmail, requires a functional EMAIL ADDRESS
    as well as an APP PASSWORD
    I recommend setting up an .env file.

    :param image_path: str, path to the image file
    :return: None
    """

    print("send email function started")
    with open(".env") as env:
        gmail_app_password = env.readline()
        email_adress = env.readline()
    email_message = EmailMessage()
    email_message["Subject"] = "Something is on the camera..."
    email_message.set_content("The camera saw something, look at the attachment")
    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(email_adress, gmail_app_password)

    # SENDER and RECEIVER are the same email adress
    gmail.sendmail(email_adress, email_adress, email_message.as_string())
    gmail.quit()

    print("send email function ended")

if __name__ == "__main__":
    send_email(image_path="images/test.png")