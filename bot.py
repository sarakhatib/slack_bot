import os
import time
import github
from slack_sdk.rtm_v2 import RTMClient
from dotenv import load_dotenv
from github import Github
from flask import Flask, request
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

token = os.environ['GITHUB_TOKEN']
g = Github(token)
github_user = g.get_user()

slack_token = os.environ["SLACK_BOT_TOKEN"]
client_slack_web = WebClient(token=slack_token)


def send_slack_message(client, txt, channel):
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=txt
        )
    except SlackApiError as e:
        assert e.response["error"]


channel_ID = "C03517LGE49"


def pr_updates(slack_client, payload):
    pr = payload["pull_request"]
    pr_id = pr["id"]
    pr_url = pr["html_url"]
    pr_title = pr["title"]
    pr_user = pr["user"]
    user_name = pr_user["login"]
    message = "Hi Users, This message is sent to tell you that a change has been made in a certain PR, see the following details:"+'\n+Pull Request ID: " + str(pr_id) + '\n' + "Pull Request URL: " + pr_url + '\n' + "Pull Request Title: " \
              + pr_title + '\n' + "Pull Request Owner: " + user_name + '\n' \
    send_slack_message(slack_client, message, channel_ID)


# Flask server
app = Flask(__name__)


@app.route('/')
def index():
    print('Hello, world! running on %s' % request.host)
    return '', 200


@app.route('/webhook', methods=['POST'])
def listen():
    print(request.json)
    pr_updates(client_slack_web, request.json)
    return '', 200


port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port, debug=True)
