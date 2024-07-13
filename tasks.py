import logging
import logging.config
from celery import Celery

# Configure logging
logging.config.fileConfig('logging.conf')

celery = Celery('tasks', broker='pyamqp://guest@localhost//')

celery.conf.update(
    result_backend='rpc://',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

@celery.task
def send_email(recipient_email):
    import smtplib
    from email.mime.text import MIMEText

    sender_email = "hng.stage3.task@gmail.com"
    sender_password = "wuzjgyvywbtkqsfo"

    msg = MIMEText("Hi! This is Mukhtar, and this is a test email sent from my Flask-Celery app! Let me know if you got this")
    msg['Subject'] = "Hello"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [recipient_email], msg.as_string())
        server.quit()
        logging.info(f"Email sent to {recipient_email}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

@celery.task
def log_time():
    from datetime import datetime
    logging.info(f'Talk to me endpoint hit at {datetime.now()}')