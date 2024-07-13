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
