import smtplib, email, ssl
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

EMAIL_ADDRESS = 'bfan.stock.ai@gmail.com'

def create_email_connection():
    context = ssl.create_default_context()
    s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, context=context)
    s.starttls()
    s.login(EMAIL_ADDRESS, 'direct3.3')
    return s

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def send_email(address, name, stocks):
    s = create_email_connection()
    message_template = read_template('message.txt')
    msg = MIMEMultipart()
    message = message_template.substitute(PERSON_NAME=name.title())
    message = message_template.substitute(STOCKS='\n'.join(stocks))
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = address
    msg['Subject'] = 'Stocks Under $20 with EMA Growth Buy Signal'

    msg.attach(MIMEText(message, 'plain'))
    s.send_message(msg)
    del msg
    s.quit()