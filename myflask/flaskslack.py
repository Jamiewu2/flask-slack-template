from threading import Thread

import requests
from flask import abort, request, jsonify

from myslack.slack import Slack, ResponseType


def parameterized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


def parameterized_decorator_instance(dec):
    """Meta-decorator that allows an instance method decorator to have parameters"""
    def layer(self, *args, **kwargs):
        def repl(f):
            return dec(self, f, *args, **kwargs)
        return repl
    return layer


def delayed_message(func: callable, response_type: ResponseType):
    """
    Sends a POST request to the response_url located in the form_content.
    See: https://api.slack.com/slash-commands#sending_delayed_responses

    :param func: The actual implementation function that does the logic.
            It should return a dict. dict should contain 'text', and/or a list of 'attachments'.
            See: https://api.slack.com/slash-commands#responding_immediate_response
    :param response_type:
    :return:
    """

    def decorator(form_content: dict):
        json_response = func(form_content)

        # send a delayed response to response_url
        response_url = form_content["response_url"]
        json_response['response_type'] = response_type.value

        requests.post(response_url, json=json_response)

    return decorator


class FlaskSlack:
    def __init__(self, slack: 'Slack'):
        self.slack = slack

    @parameterized_decorator_instance
    def slack_decorator(self, func: callable, response_type: ResponseType, verify_signature: bool=True):
        """a decorator method that wraps an implementation method to allow for receiving and responding to slack
        slash commands """
        def decorator():
            # verify that the request is from slack
            if verify_signature:
                try:
                    raw_body = request.get_data()
                    slack_request_timestamp = request.headers['X-Slack-Request-Timestamp']
                    slack_signature = request.headers['X-Slack-Signature']
                    if not self.slack.verify_signature(slack_request_timestamp, slack_signature, raw_body):
                        abort(400, {'message': 'slack verify signature failed'})
                except KeyError:
                    abort(400, {'message': 'slack verification headers missing'})

            # verification passed, handle request in another thread
            form_content = request.form
            response_type_str = response_type.value
            delayed_message_func = delayed_message(func, response_type)
            thread = Thread(target=delayed_message_func, args=(form_content,))
            thread.start()

            # immediately return 200
            return jsonify({'response_type': response_type.value})
        return decorator