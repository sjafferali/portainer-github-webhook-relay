from github_webhook import Webhook
from flask import Flask
from github import process_webhook
import logging
import os

app = Flask(__name__)
webhook = Webhook(app)


@app.route("/")
def default():
    return "Send github webhooks here"


@webhook.hook()
def on_push(data):
    process_webhook(data)


@webhook.hook()
def on_ping(data):
    return "Received Ping"


if __name__ == "__main__":
    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=LOGLEVEL)
    app.run(host="0.0.0.0", port=80)
