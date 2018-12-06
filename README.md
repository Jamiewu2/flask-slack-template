# flask-slack-template
A light decorator around flask for handling Slack slash commands


Example Usage:
```python
from myflask.flaskslack import FlaskSlack
from myslack.slack import ResponseType

flask_slack = FlaskSlack(__name__)
slack = flask_slack.slack


# set verify_signature to False if you want to do some local testing
@flask_slack.slack_route('/slack/endpoint', response_type=ResponseType.IN_CHANNEL, verify_signature=True)
def get_channel_member_ids(form_content):
    channel_id = form_content["channel_id"]
    members_form_content = slack.try_api_call("conversations.members", channel=channel_id)
    channel_member_ids = members_form_content["members"]

    text_response = f"The channel_member_ids for channel_id {channel_id} is: {channel_member_ids}"
    return {'text': text_response}


if __name__ == "__main__":
    flask_slack.run(host="localhost")
```

Installation:
 - Python3 (or just use a virtualenv)
 - Install dependencies
    - `pip install -r requirements.txt`
 - Create a file called `config.json` from `config.json.template`
    - You can find your oauth token and signing secret [here](https://api.slack.com/apps/)