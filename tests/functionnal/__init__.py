# vim:set ts=4 sw=4 et:
'''
__init__
--------
'''

import json

def is_success(response):
    """Check if response is a success
    """
    data = json.loads(response.get_data(as_text=True))
    return "Allow" in data and data["Allow"]


def post(app, payload):
    """Send a post request to /AuthZPlugin.AuthZReq'
    """
    return app.post(
        '/AuthZPlugin.AuthZReq',
        data=json.dumps(payload),
        content_type='application/json'
    )
