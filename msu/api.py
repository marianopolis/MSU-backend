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
from msu.models import Post, File, Form
from msu.events import get_events_data

bp = Blueprint('api', __name__)

def ensure_authorized():
    """Abort if user isn't an admin."""
    if g.admin_id is None:
        abort(403)


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
    posts = Post.query.order_by(Post.inserted_at.desc()).all()
    return {'data': [json_post(p) for p in posts]}

@bp.route('/api/posts/<int:id>', methods=['GET'])
def get_post(id):
    p = Post.query.get_or_404(id)
    return {'data': json_post(p)}

@bp.route('/api/posts', methods=['POST'])
def create_post():
    ensure_authorized()
    post = Post(
        subject=request.form['subject'],
        body=request.form['body'],
        admin_id=session['admin_id'],
    )
    db.session.add(post)
    db.session.flush()

    return {'data': json_post(post)}, 201

# NOTE: CURRENTLY UNIMPLEMENTED
@bp.route('/api/posts/<int:id>', methods=['PUT', 'PATCH'])
def update_post(id):
    abort(501)

@bp.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    ensure_authorized()
    p = Post.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return '', 204


@bp.route('/api/forms', methods=['GET'])
def get_forms():
    ensure_authorized()

    forms = None
    private = request.args.get('private')
    if private is None:
        forms = Form.query.all()
    elif private == 'true':
        forms = Form.query.filter_by(private=True).all()
    elif private == 'false':
        forms = Form.query.filter_by(private=False).all()
    else:
        abort(400)

    return {'data': [json_form(f) for f in forms]}

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
    files = File.query.order_by(File.desc.asc()).all()
    return {'data': [json_file(f) for f in files]}
