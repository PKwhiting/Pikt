from django.forms.widgets import ClearableFileInput

class CustomClearableFileInput(ClearableFileInput):
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            file_list = files.getlist(name)
            return file_list
        return files.get(name)

    def format_value(self, value):
        """ Return a list of file names. """
        if not value:
            return None
        if isinstance(value, list):
            return [file.name for file in value]
        return value
