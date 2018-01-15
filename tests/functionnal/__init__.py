
import json

def is_success(response):
    data = json.loads(response.get_data(as_text=True))
    return "Allow" in data and data["Allow"]


def post(app, payload):
    return app.post(
        '/AuthZPlugin.AuthZReq',
        data=json.dumps(payload),
        content_type='application/json'
    )
