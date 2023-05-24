from flask_appbuilder.fieldwidgets import BS3TextFieldWidget

class ReadOnlyField(BS3TextFieldWidget):
    def __call__(self, field, **kwargs):
        kwargs['readonly'] = 'true'
        return super(ReadOnlyField, self).__call__(field, **kwargs)