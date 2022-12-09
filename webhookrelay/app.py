from github_webhook import Webhook
from flask import Flask
from github import process_webhook

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
    print(f"received ping: {data}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
