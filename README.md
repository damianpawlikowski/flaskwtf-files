# FlaskWTF-Files
FlaskWTF-Files is a small package providing Werkzeug-aware ``MultipleFileField``
and ``FilesRequired``, ``FilesAllowed``, ``FilesSize`` validators for [Flask-WTF](https://github.com/wtforms/flask-wtf) lib.


## Why?
Currently those features are missing in the main distribution.

## Example usage:
```
from flask_wtf import FlaskForm

from flaskwtf_files import MultipleFileField
from flaskwtf_files import FilesRequired
from flaskwtf_files import FilesAllowed
from flaskwtf_files import FilesSize

# Files required
class UploadForm(FlaskForm):
    files = MultipleFileField(validators=[FilesRequired(min=1, max=5)])


# Files allowed
class UploadForm(FlaskForm):
    files = MultipleFileField(
        validators=[
            FilesAllowed(upload_set=["pdf", "txt"]),
        ]
    )

# Files size
class UploadForm(FlaskForm):
    files = MultipleFileField(
        validators=[
            # max for single file, max_total for whole upload set
            FilesSize(min=0, max=250000, max_total=900000),
        ]
    )
```

## Installing FlaskWTF-Files requirements
```
pip install -r requirements.txt
```

## Running tests
```
pip install -r tests/requirements.txt
python -m pytest tests
```

## Installation via PIP
```
Not yet available. Coming soon.
```
