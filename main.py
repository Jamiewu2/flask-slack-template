from flask import Flask

from myflask.flaskslack import FlaskSlack
from myslack.slack import ResponseType, Slack

app = Flask(__name__)
slack = Slack.create()
flask_slack = FlaskSlack(slack)


@app.route('/slack/endpoint', methods=["POST"])
# set verify_signature to False if you want to do some local testing
@flask_slack.slack_decorator(response_type=ResponseType.IN_CHANNEL, verify_signature=True)
def do_the_thing(form_content):
    text_response = f"did the thing on content: {form_content}"
    return {'text': text_response}


if __name__ == "__main__":
    app.run(host="localhost")

