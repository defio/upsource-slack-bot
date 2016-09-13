import urllib
from urllib.parse import urljoin
from urllib.parse import urlencode
import urllib.request as request
import json

# import config


def post_to_slack(json_payload):
    opener = request.build_opener(request.HTTPHandler())
    data = json_payload
    response = opener.open(request.Request('https://hooks.slack.com/services/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'), data.encode('utf-8')).read()
    print("Response: {0}".format(response.decode('utf-8')))