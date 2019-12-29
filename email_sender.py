import smtplib, email, ssl
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders 
from email.mime.base import MIMEBase 


EMAIL_ADDRESS = 'bfan.stock.ai@gmail.com'

def create_email_connection():
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(EMAIL_ADDRESS, 'direct3.3')
    return s

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def send_email(address, name, stocks, file_name):
    s = create_email_connection()
    message_template = read_template('message.txt')
    msg = MIMEMultipart()
    message = message_template.substitute(PERSON_NAME=name.title(), STOCKS='\n'.join(stocks))
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = address
    msg['Subject'] = 'Stocks Under $10 with EMA Growth Buy Signal'
    attachment = open(file_name, "rb") 
  
    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 
    
    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 
    
    # encode into base64 
    encoders.encode_base64(p) 
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % file_name)
    msg.attach(p)
    msg.attach(MIMEText(message, 'plain'))
    s.send_message(msg)
    del msg
    s.quit()