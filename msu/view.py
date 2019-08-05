from flask import (
    Blueprint,
    session,
    redirect,
    url_for,
    abort,
    request,
    render_template,
)

from .models import Admins

bp = Blueprint('view', __name__)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """login page: check for credentials"""
    # check if session is logged, if True redirect to main page
    if session.get('logged', None):
        return(redirect(url_for("view.newspage", username=session.get('username'))))

    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        user = Admins.get_by_username(username)

        session['logged'] = True
        session['username'] = username
        return redirect(url_for('view.newspage', username=username))

        # if user:
        #     true_password = user.password
        #     if password == true_password:
        #         session['logged'] = True
        #         session['username'] = username
        #         return redirect(url_for('view.newspage', username=username))
        #     else:
        #         abort(401)
        #else:
        #    return redirect(url_for('view.login'))

    return render_template('login.html')

@bp.route('/newspage/<username>', methods=['GET', 'POST'])
def newspage(username):
    """
    GET  => retrieve and display all archived and unarchived posts
    POST => add new post to database and send push notification
    """
    if session.get('logged', None):
        return render_template('newspage.html', username=username)
    else:
        abort(403)

@bp.route('/documentpage/<username>', methods=['GET', 'POST'])
def documentpage(username):
    """
    GET  => retrieve and display all available documents from file hosting
    POST => add new document and info to file hosting and postgresql db
    """
    if session.get('logged', None):
        return render_template('documentpage.html', username=username)
    else:
        abort(403)


@bp.route('/formpage/<username>', methods=['GET'])
def formpage(username):
    """
    GET => retrieve and display all available forms from postgresql db
    """
    if session.get('logged', None):
        return render_template('formpage.html', username=username)
    else:
        abort(403)

@bp.route('/logout')
def logout():
    """logout page: end session"""
    session['logged'] = False
    session.pop('username', None)
    return redirect(url_for("view.login"))
