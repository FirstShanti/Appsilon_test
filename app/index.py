from flask import g, url_for, redirect
from flask_appbuilder import IndexView
from flask_appbuilder import expose


class MovieIndexView(IndexView):

    @expose('/')
    def index(self):
        user = g.user

        if user.is_anonymous:
            return redirect(url_for('AuthDBView.login'))
        else:
            return redirect(url_for('MovieView.list'))