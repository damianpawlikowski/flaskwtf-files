from werkzeug.datastructures import FileStorage

from wtforms import MultipleFileField as _MultipleFileField


class MultipleFileField(_MultipleFileField):
    """Werkzeug-aware subclass of the :class:`wtforms.fields.MultipleFileField`."""

    def process_formdata(self, valuelist):
        valuelist = (x for x in valuelist if isinstance(x, FileStorage) and x)
        data = list(valuelist) or None

        if data is not None:
            self.data = data
        else:
            self.raw_data = ()
