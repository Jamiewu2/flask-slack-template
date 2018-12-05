# flask-slack-template
Decorator for handling Slack slash commands using flask


Example Usage:
```$xslt
from flask import Flask

from myflask.flaskslack import FlaskSlack
from myslack.slack import ResponseType, Slack

app = Flask(__name__)
slack = Slack.create()
flask_slack = FlaskSlack(slack)


@app.route('/slack/endpoint', methods=["POST"])
# set verify_signature to False if you want to do some local testing
@flask_slack.slack_decorator(response_type=ResponseType.IN_CHANNEL, verify_signature=True)
def get_channel_member_ids(form_content):
    channel_id = form_content["channel_id"]
    members_form_content = slack.try_api_call("conversations.members", channel=channel_id)
    channel_member_ids = members_form_content["members"]

    text_response = f"The channel_member_ids for channel_id {channel_id} is: {channel_member_ids}"
    print(text_response)
    return {'text': text_response}


if __name__ == "__main__":
    app.run(host="localhost")
```

Installation:
 - Python 3.6+ (or just use a virtualenv)
 - Install dependencies
    - `pip install -r requirements.txt`
 - Create config.json, see config.json.template