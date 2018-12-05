from flask import Flask

from myapp.flaskslack import FlaskSlack
app = Flask(__name__)
flask_slack = FlaskSlack()


@app.route('/slack/matrix', methods=["POST"])
@flask_slack.slack_decorator
def do_the_thing(content):
    a = f"did the thing: {content}"
    return {'text': a}

if __name__ == "__main__":
    app.run(host="localhost")


