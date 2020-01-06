"""Utility to retrieve Facebook events.

Works using Facebook's Graph API, documented at
[https://developers.facebook.com/docs/graph-api/].
"""


import urllib
import json

from dateutil.parser import isoparse


def get_events_data(group_id, access_token, since=None, until=None):
    """Retrieve events for the given ID.
    """

    url = \
        'https://graph.facebook.com/v4.0/%s/events?access_token=%s' % \
            (group_id, access_token)

    if since is not None: url += '&since=%s' % since.timestamp()
    if until is not None: url += '&until=%s' % until.timestamp()

    data = urllib.request.urlopen(url).read()
    r = json.loads(data)['data']

    # We want all API requests to return datetimes in a consistent
    # format. Thus, we parse the datetimes into python datetime objects.
    # The datetimes are stringified by the JSON encoder.
    for i in range(0, len(r)):
        for k in ['start_time', 'end_time']:
            if k in r[i]:
                r[i][k] = isoparse(r[i][k])

    return r
