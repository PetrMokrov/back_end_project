import json
import email_sender

target = {"email": "mokrov.pv@phystech.edu", "token": "https://www.w3schools.com/"}

target_compressed = json.dumps(target)

email_sender.send_email(target_compressed)

