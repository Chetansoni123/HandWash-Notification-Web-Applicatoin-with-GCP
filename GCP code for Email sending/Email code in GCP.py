import requests
import smtplib
from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading

host = "smtp.gmail.com"
port = 587
username = ""
password = ""
from_email = username
username1 = ""
password1 = ""
from_email2 = username1
to_list = []
URL = "https://handwashh.herokuapp.com/product"



def hey():
    threading.Timer(7200, hey).start()
    r = requests.get(url = URL)
    data = r.json()
    a = []
    for i in data:
        email = i["email"]
        a.append(email)
    to_list = a    
    print(to_list)
        
    if len(to_list) > 35:
        try:
            email_conn = smtplib.SMTP(host, port)
            email_conn.ehlo()
            email_conn.starttls()
            email_conn.login(username1 , password1)
            message1 = MIMEMultipart("alternative")
            message1['subject'] = "NOTIFICATION FOR HANDWASH!"
            message1['from'] = from_email2
            to_list1 = to_list[35:]
            html_txt = """\
            <html>
            <head>
            <title> Notification </title>
            </head>
            <body>
            <div id = "photo" style = "text-align: left; ">
            <span style = "vertical-align:middle"><font size = "8"> Stay Home Stay Safe!!</span>
            </div>
            <div id = "image" style = "text-align: left;">
            <span style = "vertical-align:middle"><font size = "6"><font color ="magneta">Wash Hands Regularly with Soap/Sanitizer at least 20 Seconds to stay healthy...</span>
            <p> <font color = "orange"> <font size = "4"> Go to link for this service : https://handwashh.herokuapp.com/ </p>
            </body>
            </html>
            """
            part_2 = MIMEText(html_txt, "html")
            message1.attach(part_2)
            print(message1.as_string())
            email_conn.sendmail(from_email2, to_list1, message1.as_string())
            email_conn.quit()
        except smtplib.SMTPException:
            print("error sending message")
            
            
            
        
    
    try:
        email_conn = smtplib.SMTP(host, port)
        email_conn.ehlo()
        email_conn.starttls()
        email_conn.login(username, password)    
        message = MIMEMultipart("alternative")
        message['subject'] = "NOTIFICATION FOR HANDWASH!"
        message['from'] = from_email
        to_list2 = to_list[:35]
        html_txt = """\
        <html>
        <head>
        <title> Notification </title>
        </head>
        <body>
        <div id = "photo" style = "text-align: left; ">
        <span style = "vertical-align:middle"><font size = "8"> Stay Home Stay Safe!!</span>
        </div>
        <div id = "image" style = "text-align: left;">
        <span style = "vertical-align:middle"><font size = "6"><font color ="magneta">Wash Hands Regularly with Soap/Sanitizer at least 20 Seconds to stay healthy...</span>
        <p> <font color = "orange"> <font size = "4"> Go to link for this service : https://handwashh.herokuapp.com/ </p>
        </body>
        </html>
        """
        part_1 = MIMEText(html_txt, "html")
        message.attach(part_1)
        print(message.as_string())
        email_conn.sendmail(from_email, to_list2, message.as_string())
        email_conn.quit()
            
    except smtplib.SMTPException:
        print("error sending message")


hey()



        


    
