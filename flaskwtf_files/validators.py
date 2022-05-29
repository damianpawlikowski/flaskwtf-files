from collections import abc

from werkzeug.datastructures import FileStorage

from wtforms.validators import DataRequired
from wtforms.validators import StopValidation


class FilesRequired(DataRequired):
    '''Validates if a selected files count is between `min` and `max` value and
    ensures that all the data is the
    :class:`~werkzeug.datastructures.FileStorage` object. In addition if
    `min` value is `> 0` forces required param on the
    :class:`~wtforms.fields.MultipleFileField` object.

    :param min: minimum files count, defaulted to `1`. Setting `min` to
    value `< 1` making :class:`~wtforms.fields.MultipleFileField` object
    optional.
    :param max: maximum files count, defaulted to `0`. Setting `max` to
    value `< 1` causes that unlimited number of files can be uploaded.
    :param message: validation error message, defaulted to `None`.

    Alias: `files_required`.
    '''

    def __init__(self, min=1, max=0, message=None):
        self.min = min

        if max > 0 and min > max:
            self.max = min
        else:
            self.max = max

        self.message = message

        super().__init__(self.message)
        if self.min < 1:
            self.field_flags = {'required': False}

    def __call__(self, form, field):
        default = f'''Please select atleast from {self.min} to
                  {self.max if self.max > 0 else 'unlimited number of'} files.
                  '''

        if self.min < 1:
            if not field.data:
                return

            if field.data and isinstance(field.data, abc.Iterable):
                if len(field.data) == 1:
                    if(
                        isinstance(d, FileStorage)
                            and d.content_type == 'application/octet-stream'
                            and d.content_length == 0
                            and d for d in field.data):
                        return

        if not(
            field.data
                and all(isinstance(d, FileStorage) and d for d in field.data)):
            raise StopValidation(
                self.message
                or field.gettext(default))

        if len(field.data) < self.min:
            raise StopValidation(
                self.message
                or field.gettext(default))

        if self.max < 1:
            return

        if len(field.data) > self.max:
            raise StopValidation(
                self.message
                or field.gettext(default))


files_required = FilesRequired


class FilesAllowed:
    '''Validates if a selected files have an approved extension/s
    through a passed list of extensions or the
    :class:`~flaskext.uploads.UploadSet`.

    :param upload_set: list of extensions or the
    :class:`~flaskext.uploads.UploadSet`.
    :param message: validation error message, defaulted to `None`.

    Alias: `files_allowed`.
    '''

    def __init__(self, upload_set, message=None):
        self.upload_set = upload_set
        self.message = message

    def __call__(self, form, field):
        if not(
            field.data
                and all(isinstance(d, FileStorage) and d for d in field.data)):
            return

        for data in field.data:
            filename = data.filename.lower()

            if isinstance(self.upload_set, abc.Iterable):
                if any(filename.endswith(
                        '.' + e) for e in self.upload_set):
                    continue

                raise StopValidation(
                    self.message
                    or field.gettext(
                        'Files does not have an approved extension/s: {e}'
                            .format(e=', '.join(self.upload_set))))

            if not self.upload_set.file_allowed(data, filename):
                raise StopValidation(
                    self.message
                    or field.gettext(
                        'Files does not have an approved extension/s: {e}'
                            .format(e=', '.join(self.upload_set.extensions))))


files_allowed = FilesAllowed


class FilesSize:
    '''Validates if a selected independent file size is between
    `min` and `max` value. In addition setting `min_total`/`max_total` defines
    total minimum/maximum size for an all uploads. Size values are represented
    in bytes.

    :param max: maximum independent file size. Setting `max` to value `< 1`
    causes there is no restriction.
    param min: minimum independent file size, defaulted to `0`. Setting `min`
    to value `< 1` causes there is no restriction.
    :param min_total: total minimum size for an all uploads, defaulted to `0`.
    Setting `min_total` to value `< 1` causes there is no restriction.
    :param max_total: total maximum size for an all uploads, defaulted to `0`.
    Setting `max_total` to value `< 1` causes there is no restriction.
    :param message: validation error message, defaulted to `None`.

    Alias: `files_size`.
    '''

    def __init__(self, max, min=0, min_total=0, max_total=0, message=None):
        self.min = min

        if max > 0 and min > max:
            self.max = min
        else:
            self.max = max

        self.min_total = min_total

        if max_total > 0 and min_total > max_total:
            self.max_total = min_total
        else:
            self.max_total = max_total

        self.message = message

    def __call__(self, form, field):
        if not(
            field.data
                and all(isinstance(d, FileStorage) and d for d in field.data)):
            return

        total = 0

        for i, data in enumerate(field.data):
            size = len(data.read())
            data.seek(0)

            total += size

            if self.min_total > 0:
                if i == len(field.data) - 1 and total < self.min_total:
                    raise StopValidation(
                        self.message
                        or field.gettext(
                            f'''Total upload minimum size must be
                             {self.min_total} bytes.'''))

            if self.max_total > 0:
                if size + total > self.max_total:
                    raise StopValidation(
                        self.message
                        or field.gettext(
                            f'''Total upload maximum size must be
                             {self.max_total} bytes.'''))

            if self.min > 0:
                if size < self.min:
                    raise StopValidation(
                        self.message
                        or field.gettext(
                            f'''Independent file minimum size must be
                             {self.min} bytes.'''))

            if self.max > 0:
                if size > self.max:
                    raise StopValidation(
                        self.message
                        or field.gettext(
                            f'''Independent file maximum size must be
                             {self.max} bytes.'''))


files_size = FilesSize
