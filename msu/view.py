from flask import (
    Blueprint,
    session,
    redirect,
    url_for,
    flash,
    abort,
    request,
    render_template,
)
from werkzeug.utils import secure_filename

from .models import Admins
from .functions import *

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
    if request.method == 'POST':
        formType = request.form['form_type']

        if formType == 'add':
            postTitle = request.form['title']
            postAuthor = request.form['author']
            postContent = request.form['text']
            sendNotif = request.form['notif']

            #create_post(postTitle, postContent, postAuthor)

            if sendNotif == 'on':
                pass # send push notifs to frontend

        elif formType == 'delete':
            postID = request.form['id']
            #delete_post(postID)

    #all_posts = get_posts() # unarchived posts


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

    if request.method == 'POST':
        formType = request.form['form_type']

        if formType == 'add':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No file selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                fileName = (request.form['filename'].split('.')[0]) + '.' + (file.filename.split('.')[-1])
                fileName = secure_filename(fileName)
                fileDescription = request.form['description']
                fileAuthor = request.form['author']
                sendNotif = request.form['notif']

                upload_document(file, fileName, fileDescription, fileAuthor)
                flash('File successfully uploaded')

                if sendNotif == 'on':
                    pass # send push notifs to frontend
            else:
                flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
                return redirect(request.url)

        elif formType == 'delete':
            documentID = request.form['id']
            delete_document(documentID)


    #all_documents = get_documents()

    if session.get('logged', None):
        return render_template('documentpage.html', username=username)
    else:
        abort(403)


@bp.route('/formpage/<username>', methods=['GET'])
def formpage(username):
    """
    GET => retrieve and display all available forms from postgresql db
    POST => delete form
    """

    if request.method == 'POST':
        formID = request.form['id']
        #delete_form(formID)

    #user = Admins.get_by_username(session['username'])
    #isAdmin = user.admin

    #public_forms = get_forms(private=False)

    #if isAdmin: private_forms = get_forms(private=True)
    #else: private_forms = []


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
