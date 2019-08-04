import datetime

def get_posts(get_archived=False):
    """retrieve archived or unarchived posts from database"""
    if get_archived:
        archived_posts = Posts.query.filter_by(archived=True).order_by(desc(Posts.uploadtime)).all()
        return archived_posts
    else:
        unarchived_posts = Posts.query.filter_by(archived=False).order_by(desc(Posts.uploadtime)).all()
        return unarchived_posts

def create_post(title, text, author):
    """create new post class and add it to the database"""
    title = title.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")
    text = text.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")
    author = author.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")

    new_post = Posts(title=title, text=text, author=author, uploadtime=datetime.datetime.now())
    db.session.add(new_post)
    db.session.commit()

def get_documents():
    """retrieve all documents from database with corresponding description and download link"""
    documents = Documents.query.order_by(desc(Documents.uploadtime)).all()
    return documents

def upload_document(file, filename, description, author, uploadtime):
    # store document data in file hosting server and get file access url (file_url)

    new_document = Documents(filename=filename, file_url=file_url, description=description, author=author, uploadtime=datetime.datetime.now())
    db.session.add(new_document)
    db.session.commit()

def get_forms():
    """retrive all forms from database"""
    forms = Forms.query.order_by(desc(Forms.uploadtime)).all()
    return forms

def upload_form(name, subject, message):
    """create new form object class and add to database"""
    new_form = Forms(name=name, subject=subject, message=message, uploadtime=uploadtime)
    db.session.add(new_form)
    db.session.commit()
