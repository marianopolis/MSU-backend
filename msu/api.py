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

def check_authorized():
    if g.admin_id is None:
        abort(403)

def fmt_time(time):
    return time.strftime("%b %d, %Y")

def json_post(post):
    return {
        'id': post.id,
        'subject': post.subject,
        'body': post.body,
        'inserted_at': fmt_time(post.inserted_at),
    }

def json_form(form):
    r = {
        'id': form.id,
        'subject': form.subject,
        'body': form.body,
        'private': form.private,
        'inserted_at': fmt_time(form.inserted_at),
    }

    if form.name is not None:
        r['name'] = form.name

    return r

def json_file(file):
    return {
        'key': file.key,
        'desc': file.desc,
        'url': file.url,
        'version': file.version,
        'inserted_at': fmt_time(file.inserted_at),
    }

@bp.route('/api/events', methods=['GET'])
def get_events():
    group_id = current_app.config['FB_GROUP_ID']
    access_tok = current_app.config['FB_ACCESS_TOKEN']

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
    check_authorized()
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
    check_authorized()
    p = Post.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return '', 204


@bp.route('/api/forms', methods=['GET'])
def get_forms():
    check_authorized()

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
