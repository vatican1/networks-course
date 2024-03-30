import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

if __name__ == "__main__":
    for message_type in ['txt', 'html']:
        receiver_email = 'vatican2001@gmail.com'
        sender_email = 'vitya-zakharov-2025@mail.ru'
        password = '...' # тут пришлось создавать специальный пароль для внешних приложений

        if message_type == 'txt':
            message = MIMEText('Hello, this is a text message.')
        elif message_type == 'html':
            message = MIMEText('<html><body><h1>Hello, this is an HTML message.</h1></body></html>', 'html')

        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = 'Test Email'

        server = smtplib.SMTP('smtp.mail.ru', 587) #mail

        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

