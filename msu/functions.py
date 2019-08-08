import datetime

def get_posts(get_archived=False):
    """retrieve archived or unarchived posts from database"""
    if get_archived: posts = Posts.query.filter_by(archived=True).order_by(desc(Posts.uploadtime)).all()
    else: posts = Posts.query.filter_by(archived=False).order_by(desc(Posts.uploadtime)).all()
    return posts

def create_post(title, text, author):
    """create new post class and add it to the database"""
    title = title.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")
    text = text.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")
    author = author.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")

    new_post = Posts(title=title, text=text, author=author, uploadtime=datetime.datetime.now())
    db.session.add(new_post)
    db.session.commit()

def delete_post(id_):
    post_to_delete = Posts.query.get(id_)
    db.session.delete(post_to_delete)
    db.session.commit()

def get_documents():
    """retrieve all documents from database with corresponding description and download link"""
    documents = Files.query.order_by(desc(Files.uploadtime)).all()
    return documents
    

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_document(file, filename, description, author):
    # store document data in file hosting server and get file access url (file_url)

    new_document = Files(filename=filename, file_url=file_url, description=description, author=author, uploadtime=datetime.datetime.now())
    db.session.add(new_document)
    db.session.commit()

def delete_document(id_):
    file_to_delete = Files.query.get(id_)
    file_url = file_to_delete.file_url

    # delete document data from file hosting server using file url

    db.session.delete(file_to_delete)
    db.session.commit()

def get_forms(private=False):
    """retrive all forms from database"""
    if private: forms = Forms.query.filter_by(private=True).order_by(desc(Forms.uploadtime)).all()
    else: forms = Forms.query.filter_by(private=False).order_by(desc(Forms.uploadtime)).all()
    return forms

def upload_form(name, subject, message):
    """create new form object class and add to database"""
    new_form = Forms(name=name, subject=subject, message=message, uploadtime=datetime.datetime.now())
    db.session.add(new_form)
    db.session.commit()

def delete_form(id_):
    form_to_delete = Forms.query.get(id_)
    db.session.delete(form_to_delete)
    db.session.commit()
