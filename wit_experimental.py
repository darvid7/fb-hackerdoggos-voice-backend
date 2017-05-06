from wit import Wit

# Read access token for wit.ai instance.
with open('wit_server_config', 'r') as f:
    config = f.readlines()

access_token = config[0].strip()

wit_client = Wit(access_token=access_token)

wit_resp = wit_client.message('When is Tom\'s birthday?')
print(wit_resp)
