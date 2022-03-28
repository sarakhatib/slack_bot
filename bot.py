import os
import time

import github
from slack_sdk.rtm_v2 import RTMClient
from dotenv import load_dotenv
from github import Github

# from pprint import pprint

from flask import Flask, request

load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    # return "Hello World!"
    return 'Hello, world! running on %s' % request.host


@app.route('/Webhook', methods=['POST'])
def listen():
    print(request.get_json())
    return 200


# port = os.environ["PORT"]
# app.run()
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)

token = os.environ['GITHUB_TOKEN']
g = Github(token)
rtm = RTMClient(token=os.environ["SLACK_BOT_TOKEN"])
github_user = g.get_user()


# repos = user.get_repos()
#
# for repo in repos:
#     print(repo.name)
#     pull_requests = repo.get_pulls()
#     for pull in pull_requests:
#         print(pull.get_comments())


@rtm.on("message")
def handle(client: RTMClient, event: dict):
    if 'Hello' in event['text']:
        hello_handler(client, event)
    elif 'Pull Request' in event['text'] or 'PR' in event['text']:
        PR_handler(client, event)
    else:
        client.web_client.chat_postMessage(
            channel=event['channel'],
            text="nope"
        )


def hello_handler(client: RTMClient, event: dict):
    channel_id = event['channel']
    thread_ts = event['ts']
    user = event['user']  # This is not username but user ID (the format is either U*** or W***)

    client.web_client.chat_postMessage(
        channel=channel_id,
        text=f"Hi <@{user}>!"
    )

# def PR_handler(client: RTMClient, event: dict):
#     channel_id = event['channel']
#     thread_ts = event['ts']
#     user = event['user']  # This is not username but user ID (the format is either U*** or W***)
#
#     client.web_client.chat_postMessage(
#         channel=channel_id,
#         text="send me a number"
#     )
#     time.sleep(15)
#
#     @rtm.on("message")
#     def response():
#         client.web_client.chat_postMessage(
#             channel=channel_id,
#             text="okay got it"
#         )


# rtm.start()
