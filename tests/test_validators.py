import os
import tempfile

import pytest

from werkzeug.datastructures import FileStorage

from flaskwtf_files.validators import FilesRequired
from flaskwtf_files.validators import FilesAllowed
from flaskwtf_files.validators import FilesSize


@pytest.mark.parametrize('min, max', [(0, 2), (1, 2)])
def test_files_required(upload_form, min, max):
    form = upload_form()
    form.files.validators = [FilesRequired(min=min, max=max)]
    files = [
        FileStorage(filename='test.txt'),
        FileStorage(filename='test.docx')]

    if min <= 0:
        assert form.validate()
    else:
        assert not form.validate()

    form.files.data = files
    assert form.validate()

    files.append(FileStorage(filename='test.pdf'))
    form.files.data = files
    assert not form.validate()


def test_files_allowed(upload_form):
    form = upload_form()
    form.files.validators = [FilesAllowed(['txt'])]
    files = [
        FileStorage(filename='test.txt'),
        FileStorage(filename='test.docx')]
    form.files.data = files

    assert not form.validate()

    form.files.validators = [FilesAllowed(['txt', 'docx'])]
    assert form.validate()


def test_files_allowed_upload_set(app, upload_form):
    pytest.importorskip('flask_uploads')
    from flask_uploads import UploadSet, configure_uploads

    app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
    upload_set = UploadSet('test', extensions=['txt'])
    configure_uploads(app, upload_set)
    form = upload_form()
    files = [
        FileStorage(filename='test.txt'),
        FileStorage(filename='test.docx')]
    form.files.data = files

    form.files.validators = [FilesAllowed(upload_set)]
    assert not form.validate()

    upload_set = UploadSet('test', extensions=['txt', 'docx'])
    form.files.validators = [FilesAllowed(upload_set)]
    assert form.validate()


@pytest.mark.parametrize(
    'max, min, min_total, max_total', ([(100, 5, 0, 0), (100, 5, 11, 101)]))
def test_files_size(upload_form, max, min, min_total, max_total):
    form = upload_form()
    form.files.validators = [FilesSize(max, min, min_total, max_total)]

    with tempfile.TemporaryFile() as file:
        file.write(os.urandom(min-1))
        file.seek(0)
        form.files.data = [FileStorage(file)]
        assert not form.validate()

        if min_total <= 0:
            file.write(os.urandom(min))
            file.seek(0)
            form.files.data = [FileStorage(file)]
            assert form.validate()

        file.write(os.urandom(max+1))
        file.seek(0)
        form.files.data = [FileStorage(file)]
        assert not form.validate()

        if min_total > 0:
            file.write(os.urandom(min+1))
            file.seek(0)
            form.files.data = [FileStorage(file), FileStorage(file)]
            assert not form.validate()

        if max_total > 0:
            file.write(os.urandom(max+1))
            file.seek(0)
            form.files.data = [FileStorage(file), FileStorage(file)]
            assert not form.validate()
