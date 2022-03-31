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
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'


rtm = RTMClient(token=os.environ["SLACK_BOT_TOKEN"])
channel_ID = "C03517LGE49"


# @rtm.on("message")
# def handle(client: RTMClient, event: dict):
#     print("got in")
#     print(client)
#     channel_id = event['channel']
#     user = event['user']  # This is not username but user ID (the format is either U*** or W***)
#     client.web_client.chat_postMessage(
#         channel=channel_id,
#         text=f"Hi <@{user}>!"
#     )
#
# rtm.start()

def pr_updates(slack_client, payload):
    pr = payload["pull_request"]
    pr_id = pr["id"]
    pr_url = pr["html_url"]
    pr_title = pr["title"]
    pr_user = pr["user"]
    user_name = pr_user["login"]
    # created_at = payload["created_at"]
    # updated_at = payload["updated_at"]
    # closed_at = payload["closed_at"]
    # merged_at = payload["merged_at"]
    #repo = pr["repo"]
    #repo_id = repo["id"]
    #repo_name = repo["name"]
    # comments = payload["_links"]["comments"]
    # comments_url = requests.get(comments)
    # comments_arr = []
    # for comment in comments_url:
    #     comments_arr.append(comments_url["body"])
    # message = {"Pull Request ID": pr_id, "Pull Request URL": pr_url, "Pull Request Title": pr_title,
    #            "Pull Request Owner": user_name, "Created at": created_at, "Updated at": updated_at,
    #            "Closed at": closed_at, "Merged at": merged_at, "Repository ID": repo_id, "Repository Name": repo_name,
    #            "Comments": comments_arr}
    message = "Pull Request ID: " + str(pr_id) + '\n' + "Pull Request URL: " + pr_url + '\n' + "Pull Request Title: " \
              + pr_title + '\n' + "Pull Request Owner: " + user_name + '\n' \
              #+ "Repository ID: " \+ repo_id + '/n' + "Repository Name: " + repo_name
    send_slack_message(slack_client, message, channel_ID)


send_slack_message(client_slack_web, "hello", channel_ID)
# Flask server
app = Flask(__name__)


@app.route('/')
def index():
    # return "Hello World!"
    print('Hello, world! running on %s' % request.host)
    return '', 200


@app.route('/webhook', methods=['POST'])
def listen():
    print(request.json)
    pr_updates(client_slack_web, request.json)
    return '', 200


port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port, debug=True)
