from flask import Flask, session, render_template, request, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from functions import get_posts, create_post, get_documents, upload_document, get_forms, upload_form
import datetime
import config
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


'''from models import Users, Posts, Documents, Forms'''         # import datatables from postgresql database


# API routes for interaction with frontend application

@app.route('/api/posts')
def api_post():
    """route description: GET => return all unarchived posts"""
    if not session.get('logged', None): abort(403)
    return get_posts(get_archived=False)

@app.route('/api/files')
def api_files():
    """route description: GET => return all file descriptions and urls"""
    if not session.get('logged', None): abort(403)
    return get_documents()

@app.route('/api/forms', methods=['GET', 'POST'])
def api_forms():
    """route description: POST => add new form submitted by user to database"""
    if not session.get('logged', None): abort(403)
    if request.method == 'POST':
        # get name, subject, message from post request
        upload_form(name, subject, message)
        return "Form upload was successful"


# routes for admin interaction with webapp

@app.route('/', methods=['GET','POST'])
@app.route('/login')
def index():
    """login page: check for credentials"""
    if session.get('logged', None): return(redirect(\
                    url_for("newspage", username=session.get('username'))))     # check if session is logged, if True redirect to main page
    if request.method == 'POST':
        username = request.form.get('username', None)                           # get username inputted from form
        password = request.form.get('password', None)                           # get password inputted from form
        user = Users.query.filter_by(username=username).first()                 # query Users table for inputted username

        if user:                                        
            true_password = user.password                                       # if username exists, retrieve user password
            if password == true_password:
                session['logged'] = true_password                               # set session variable to True
                session['username'] = username                                  # set session username
                return redirect(url_for('addnews', username=username))          # if user password == inputted password, redirect to main page
        else: return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/newspage/<username>', methods=['GET', 'POST'])                     
def newspage(username):
    """newspage description: GET => retrieve and display all archived and unarchived posts; 
    POST => add new post to database and send push notification"""
    if not session.get('logged', None): abort(403)
    return render_template('newspage.html', username=username)


@app.route('/documentpage/<username>', methods=['GET', 'POST'])                 
def documentpage(username):
    """documentpage description: GET => retrieve and display all available documents from file hosting; 
    POST => add new document and info to file hosting and postgresql db"""
    if not session.get('logged', None): abort(403)
    return render_template('documentpage.html', username=username)


@app.route('/formpage/<username>', methods=['GET'])                             
def formpage(username):
    """formpage description: GET => retrieve and display all available forms from postgresql db"""
    if not session.get('logged', None): abort(403)
    return render_template('formpage.html', username=username)


@app.route('/logout')                                                           
    def logout():
        """logout page: end session"""
        session['logged'] = False                                               # set session variable to False
        session.pop('username', None)
        return redirect(url_for("login"))



if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)