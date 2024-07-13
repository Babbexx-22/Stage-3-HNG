# Messaging System with RabbitMQ/Celery and Python Application behind Nginx

This project demonstrates how to set up a Flask application with Celery for background task processing and how to expose the application using ngrok.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Running ngrok](#running-ngrok)
- [Running in the Background](#running-in-the-background)
- [Using Celery](#using-celery)
- [Endpoints](#endpoints)
- [Logging](#logging)
- [License](#license)

## Requirements

- Python 3.6+
- Flask
- nginx
- Celery
- RabbitMQ (as Celery broker)
- ngrok

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Babbexx-22/Stage-3-HNG.git
    cd yourrepository
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate 
    ```

3. Install the dependencies:

    ```bash
    pip install flask celery
  ```
4. Install nginx and configure it to route request to your python backend. Edit your instance IP

```
sudo nano /etc/nginx/sites-available/messaging_log.conf
server {
    listen 80;
    server_name instance-IP;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```

## Configuration

### Celery Configuration and tasks distribution details

Update the tasks.py file with the appropriate broker URL:

```
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
)

```

## Logging Configuration

Create a logging.conf file:

```
[loggers]
keys=root

[handlers]
keys=hand01

[formatters]
keys=form01

[logger_root]
level=DEBUG
handlers=hand01

[handler_hand01]
class=FileHandler
level=INFO
formatter=form01
args=('/var/log/messaging_system.log', 'a')

[formatter_form01]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s

```

## main.py file configuration

```
from flask import Flask, request
from tasks import send_email, log_time
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def index():
    if 'sendmail' in request.args:
        recipient = request.args.get('sendmail')
        send_email.delay(recipient)
        return f'Email will be sent to {recipient}'
    elif 'talktome' in request.args:
        current_time = datetime.now()
        result = log_time.delay()
        return f'Time logged at {current_time}!'
    else:
        return 'Invalid parameters, Please try to access /?sendmail=your_mail.com or /?talktome'

if __name__ == '__main__':
    app.run(debug=True)

```

## Running the Application

Start Flask Application 

In your app directory, create a virtual environment, activate it and run your flask application in the background using nohup

```
python -m venv venv
source venv/bin/activate
nohup python main.py > flask_app.log 2>&1 &

```

Start celery worker

```
python -m venv venv
source venv/bin/activate
nohup celery -A tasks worker --loglevel=info > celery_worker.log 2>&1 &

```

Running ngrok
Install ngrok and finish up the necessary configuration and authentication.
Run ngrok in the background

` nohup ngrok http 5000 `

