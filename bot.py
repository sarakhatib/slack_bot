import os
import time
import github
from slack_sdk.rtm_v2 import RTMClient
from dotenv import load_dotenv
from github import Github
from flask import Flask, request
import requests

load_dotenv()

token = os.environ['GITHUB_TOKEN']
g = Github(token)
github_user = g.get_user()

rtm = RTMClient(token=os.environ["SLACK_BOT_TOKEN"])

# repos = user.get_repos()
# for repo in repos:
#     print(repo.name)
#     pull_requests = repo.get_pulls()
#     for pull in pull_requests:
#         print(pull.get_comments())

channel_ID = "C03517LGE49"


@rtm.on("message")
def handle(client: RTMClient, event: dict):
    channel_id = event['channel']
    user = event['user']  # This is not username but user ID (the format is either U*** or W***)
    client.web_client.chat_postMessage(
        channel=channel_id,
        text=f"Hi <@{user}>!"
    )


def pr_updates(payload):
    # pr = json["pull_request"]
    # pr_id = pr["id"]
    # pr_url = pr["html_url"]
    # pr_title = pr["title"]
    # pr_user = pr["user"]
    # user_name = pr_user["login"]
    # created_at = json["created_at"]
    # updated_at = json["updated_at"]
    # closed_at = json["closed_at"]
    # merged_at = json["merged_at"]
    # repo = json["repo"]
    # repo_id = repo["id"]
    # repo_name = repo["name"]
    # comments = json["_links"]["comments"]
    # comments_url = requests.get(comments)
    # comments_arr = []
    # for comment in comments_url:
    #     comments_arr.append(comments_url["body"])
    # message = {"Pull Request ID": pr_id, "Pull Request URL": pr_url, "Pull Request Title": pr_title,
    #            "Pull Request Owner": user_name, "Created at": created_at, "Updated at": updated_at,
    #            "Closed at": closed_at, "Merged at": merged_at, "Repository ID": repo_id, "Repository Name": repo_name,
    #            "Comments": comments_arr}
    # json_message = json.dumps(message)
    rtm.web_client.chat_postMessage(
        channel=channel_ID,
        text=str(payload)
    )


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
    pr_updates(request.json)
    return '', 200


port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port, debug=True)

#rtm.start()
