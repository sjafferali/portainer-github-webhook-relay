from github_webhook import Webhook
from flask import Flask
from github import process_webhook

app = Flask(__name__)
webhook = Webhook(app)


@webhook.hook()
def on_push(data):
    process_webhook(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
