import smtplib, ssl
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# configuration
with open("email_config.json", 'r') as config_file:
  config = json.load(config_file)

email_server = config['server_email']
email_port = config['port_email']
sender_email = config["sender_email"]
password = config["password"]

def send_email(received_target) :
  target = json.loads(received_target)
  receiver_email = target["email"]
  token = target['token']
  with open("templates/message.html", "r") as html:
    html_body = html.read()
  html_body = html_body.format(token)

  message = MIMEMultipart("alternative")
  message["Subject"] = "Email Confirmation"
  message["From"] = sender_email
  message["To"] = receiver_email

  to_attach = MIMEText(html_body, "html")
  message.attach(to_attach)

  # Create secure connection with server and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(email_server, email_port, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(
          sender_email, receiver_email, message.as_string()
      )
