import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SendMail():
    def __init__(self, content):
        # Create a multipart message and set headers
        password = content["password"]

        message = MIMEMultipart()
        message["From"] = content['sender_email']
        message["To"] = content['receiver_email']
        message["Subject"] = content['subject']

        # Add body to email
        message.attach(MIMEText(content['body'], "plain"))

        directory = content['directory']
        filename = content['filename']

        # Open PDF file in binary mode
        with open(directory+filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(content['sender_email'], content['password'])
            server.sendmail(content['sender_email'], content['receiver_email'], text)

