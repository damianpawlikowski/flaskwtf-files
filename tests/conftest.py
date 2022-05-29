import pytest

from flask import Flask

from flask_wtf import FlaskForm

from flaskwtf_files.fields import MultipleFileField


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = '9a644a3f15ef7010660ccfa512c2afd1'

    return app


@pytest.fixture
def app_ctx(app):
    with app.app_context() as app_ctx:
        yield app_ctx


@pytest.fixture
def req_ctx(app):
    with app.test_request_context() as req_ctx:
        yield req_ctx


@pytest.fixture()
def upload_form(req_ctx):
    class UploadForm(FlaskForm):
        class Meta:
            csrf = False

        files = MultipleFileField()

    return UploadForm
