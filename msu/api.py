from flask import Blueprint, session, abort, request

from .models import Post, File, Form

bp = Blueprint('api', __name__)

@bp.route('/api/posts')
def api_post():
    """
    GET => return all unarchived posts
    """
    if session.get('logged', None):
        return Post.query.all()
    else:
        abort(403)

@bp.route('/api/files')
def api_files():
    """
    GET => return all file descriptions and urls
    """
    if session.get('logged', None):
        return File.query.all()
    else:
        abort(403)

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
