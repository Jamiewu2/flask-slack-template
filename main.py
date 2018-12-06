from flask import Flask

from flaskslack.flaskslack import FlaskSlack
from flaskslack.slack import ResponseType, Slack

app = Flask(__name__)
# If you want to get your config in a non default way,
# you can create a slack client with: Slack('slack_oauth_token', 'slack_signing_secret')
slack = Slack.create()
flask_slack = FlaskSlack(app, slack)


# set verify_signature to False if you want to do some local testing
@flask_slack.slack_route('/slack/endpoint', response_type=ResponseType.IN_CHANNEL, verify_signature=True)
def get_channel_member_ids(form_content):
    """
    :param form_content: a dict containing the data payload from the slack HTTP POST
            see: https://api.slack.com/slash-commands#app_command_handling
    :return: It should return a dict. The dict should contain a 'text' field, and/or a list of 'attachments'.
            see: https://api.slack.com/slash-commands#responding_immediate_response
    """

    channel_id = form_content["channel_id"]
    members_form_content = slack.try_api_call("conversations.members", channel=channel_id)
    channel_member_ids = members_form_content["members"]

    text_response = f"The channel_member_ids for channel_id {channel_id} is: {channel_member_ids}"
    return Slack.create_response(text_response)


if __name__ == "__main__":
    app.run(host="localhost")
