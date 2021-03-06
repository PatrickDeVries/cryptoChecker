import requests
import pandas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename



def sendNotif(subject, message, sender, destination, files=None):
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
    
    for f in files or []:
        with open(f, 'rb') as fil:
            part = MIMEApplication(
            fil.read(),
            Name=basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)
    
    
    msg.attach(MIMEText(message))
    server.sendmail(sender, destination, msg.as_string())
    server.quit()
