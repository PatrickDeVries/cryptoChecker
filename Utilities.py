import requests
import pandas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendNotif(subject, message, sender, destination):
    # Start connection
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # File containing login info for gmail account that will send messages
    logininfo = open('devpass.txt')
    lines = logininfo.readlines()
    server.login(lines[0], lines[1])
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = destination
    msg.attach(MIMEText(message))
    server.sendmail(sender, destination, msg.as_string())
    server.quit()
