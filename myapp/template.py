class Template:
    def __init__(self):
        pass

    # def do_matrix(self, content):
    #     channel_id = content["channel_id"]
    #     response_url = content["response_url"]
    #     response = try_api_call("conversations.members", channel=channel_id)
    #     channel_members = response["members"]
    #     user_names = list(map(get_name_from_user_id, channel_members))
    #     rotated_user_names = user_names[1:] + user_names[:1]
    #     pairs = [(user_names[x], rotated_user_names[x]) for x in range(len(user_names))]
    #     payload = {'response_type': 'in_channel',
    #                'text': pprint_pairs(pairs)}
    #     requests.post(response_url, json=payload)
    #     return payload
    #
    # def pprint_pairs(pairs):
    #     str_list = ['```']
    #     for pair in pairs:
    #         str_list.append("{:30} | {:30}".format(pair[0], pair[1]))
    #     str_list.append("```")
    #     return "\n".join(str_list)
    #
    #
    # def try_api_call(api_call_method: str, **kwargs) -> dict:
    #     response = slack.api_call(api_call_method, **kwargs)
    #     if "error" in response:
    #         pp.pprint(response)
    #         raise Exception("Error occurred during api call")
    #     return response
    #
    #
    # def get_name_from_user_id(user_id):
    #     response = try_api_call("users.info", user=user_id)
    #     return response["user"]["real_name"]