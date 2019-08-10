from flask import Blueprint, session, abort, request

from msu import db
from msu.models import Post, File, Form

bp = Blueprint('api', __name__)

def check_authorized():
    if not session.get('logged', None):
        abort(403)

def json_post(post):
    return {
        'id': post.id,
        'subject': post.subject,
        'body': post.body,
        'inserted_at': post.inserted_at,
    }

@bp.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return {'data': [ json_post(p) for p in posts]}

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

@bp.route('/api/forms', methods=['GET', 'POST'])
def api_forms():
    """
    POST => add new form submitted by user to database
    """
    if not session.get('logged', None):
        abort(403)

    if request.method == 'POST':
        db.session.add(Form(
            name=request.form['name'],
            subject=request.form['subject'],
            message=request.form['message'],
        ))
        db.commit()

        return "", 201
