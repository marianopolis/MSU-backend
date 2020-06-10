"""REST resources to be consumed by clients.

This module defines all the REST API routes provided by the
application. All returned data MUST be wrapped in a `data`
key as such:

    {
      "data": ...data to be returned...
    }

This module loosely follows the Microsoft REST API design guidelines,
which can be seen at
[https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design].
"""

from flask import (
    Blueprint,
    session,
    abort,
    request,
    g,
    current_app,
)

from msu import db
from msu.models import Post, File, Link, Form, CongressMember
from msu.events import get_events_data
from msu.calendar import list_events
import datetime

bp = Blueprint('api', __name__)

# The json_* format the given objects into
# dictionaries which are returned by the API
# as JSON data.
def json_post(post: Post):
    return {
        'id': post.id,
        'subject': post.subject,
        'body': post.body,
        'inserted_at': post.inserted_at,
        'updated_at': post.updated_at,
    }

def json_form(form: Form):
    r = {
        'id': form.id,
        'subject': form.subject,
        'body': form.body,
        'private': form.private,
        'inserted_at': form.inserted_at,
    }

    if form.name is not None:
        r['name'] = form.name

    return r

def json_file(file: File):
    return {
        'key': file.key,
        'desc': file.desc,
        'url': file.url,
        'inserted_at': file.inserted_at,
        'updated_at': file.updated_at,
    }

def json_link(link: Link):
    return {
        'desc': link.desc,
        'url': link.url,
        'inserted_at': link.inserted_at,
        'updated_at': link.updated_at,
    }

def json_congress_member(cm: CongressMember):
    return {
        'name': cm.name,
        'title': cm.title,
        'url': cm.file.url,
    }

@bp.route('/api/congress', methods=['GET'])
def get_congress():
    congressmembers = CongressMember.query.order_by(CongressMember.id.asc()).all()
    return {'data': [json_congress_member(c) for c in congressmembers]}

@bp.route('/api/events', methods=['GET'])
def get_events():
    group_id = current_app.config['FB_GROUP_ID']
    access_tok = current_app.config['FB_ACCESS_TOKEN']

    if group_id is None or access_tok is None:
        return '', 503

    data = get_events_data(group_id, access_tok)
    return {'data': data}

@bp.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query \
        .filter(Post.archived == False) \
        .order_by(Post.inserted_at.desc()) \
        .all()
    return {'data': [json_post(p) for p in posts]}

@bp.route('/api/forms', methods=['POST'])
def create_form():
    if not request.is_json:
        abort(400)

    data = request.get_json()
    db.session.add(Form(
        name=data.get('name'),
        private=data.get('private'),
        subject=data['subject'],
        body=data['body'],
    ))
    db.session.commit()
    return '', 201

@bp.route('/api/files', methods=['GET'])
def get_files():
    files = File.query.filter_by(hidden=False) \
                .order_by(File.desc.asc()).all()
    return {'data': [json_file(f) for f in files]}

@bp.route('/api/links', methods=['GET'])
def get_links():
    links = Link.query.order_by(Link.desc.asc()).all()
    return {'data': [json_link(f) for f in links]}

# union of files and links
@bp.route('/api/resources', methods=['GET'])
def get_resources():
    files = map(json_file, File.query.filter_by(hidden=False).all())
    links = map(json_link, Link.query.all())
    r = list(files) + list(links)
    r.sort(key=(lambda x: x['updated_at']), reverse=True)
    return {'data': r}

@bp.route('/api/calendar', methods=['GET'])
def get_cal_events():
    events = list_events(
        num=request.args.get('num'),
        since=request.args.get('since'),
    )
    return {'data': events}
