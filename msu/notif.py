import sys
import json
from flask import current_app as app
import firebase_admin as fb
import firebase_admin.messaging as fcm

from .models import PushNotifDevice

def _init_app():
    json_data = app.config['FIREBASE_SERVICE_ACCOUNT_JSON']
    if json_data is not None:
        cert = json.loads(json_data)
        cred = fb.credentials.Certificate(cert)
        return fb.initialize_app(credential=cred)
    else:
        print('$FIREBASE_SERVICE_ACCOUNT_JSON not set. '
              'Push notifications are disabled', file=sys.stderr)
        return None

fb_app = _init_app()

def _msg(token, title, body, data):
    return fcm.Message(
        data={"data": json.dumps(data)},
        token=token,
        notification=fcm.Notification(
            title=title,
            body=body,
        ),
    )

def _notify(tokens, title, body, data):
    if fb_app is None:
        print('Push not configured')
        return

    msgs = [_msg(t, title, body, data) for t in tokens]
    fcm.send_all(msgs, dry_run=False, app=fb_app)

def send(title, body, data):
    tokens = [d.token for d in PushNotifDevice.query.all()]
    _notify(tokens, title, body, data)
