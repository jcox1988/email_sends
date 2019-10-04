import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender, recipient, subject, message, **kwargs):
    '''
    This function sends an email. 
    It requires the email address that will send the message, 
    the email address that receive the message,
    the subject of the email, and the message.
    You can optionally provide any emails that will be cc'ed.
    CC'ed address must be provided as a list with a key of 'cc'.
    '''
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    to_list = [recipient]
    if 'cc' in kwargs:
        msg['Cc'] =  ','.join(kwargs.get('cc'))
        for address in kwargs.get('cc'):
            to_list.append(address)
    #TODO: Attachments
    msg.attach(MIMEText(message, 'html'))
    mailServer = smtplib.SMTP('mail.smtp2go.com',587)
    mailServer.starttls()
    mailServer.login(sender, 'email_password')
    text = msg.as_string()
    mailServer.sendmail(sender, to_list, text)
    del msg
    mailServer.quit()