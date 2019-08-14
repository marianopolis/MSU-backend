import pytest

from msu import create_app, db
from msu.models import Admin, Post, File, Form

app = create_app(testing=True)

@pytest.fixture
def sess():
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.close()
        db.drop_all()

def test_admin(sess):
    sess.add(Admin(
        username='user',
        password='pass',
        name='Bob',
    ))
    sess.commit()

    admin = Admin.query.filter_by(username='user').first()

    assert admin.password_equals('pass')
    assert admin.id

def test_post(sess):
    sess.add(Admin(
        username='user',
        password='pass',
        name='Bob',
    ))
    sess.commit()

    admin = Admin.query.filter_by(username='user').first()

    sess.add(Post(
        subject='Title',
        body='Hello World!',
        admin_id=admin.id,
    ))
    sess.commit()

    post = Post.query.first()

    assert post.subject == 'Title'
    assert post.body == 'Hello World!'

@pytest.mark.skip(reason="Uploads to S3")
def test_file(sess):
    sess.add(File(
        key='file.png',
        desc='A picture of something',
        data=b'',
    ))
    sess.commit()

    file = File.query.first()

    assert file.key == 'file.png'
    assert file.desc == 'A picture of something'
    assert file.data == b''

def test_form(sess):
    sess.add(Form(
        name='Bob',
        subject='Title',
        body='Hello World!',
    ))
    sess.commit()

    form = Form.query.first()

    assert form.name == 'Bob'
    assert form.subject == 'Title'
    assert form.body == 'Hello World!'
