from flask import render_template, redirect, flash, url_for
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from flask_appbuilder.actions import action
from wtforms import StringField
from .forms import ReadOnlyField

from app import appbuilder, db

from app.models import Movie


class MovieView(ModelView):
    datamodel = SQLAInterface(Movie)

    list_columns = ['title','released_at','imdb_id', 'wiki_entity_id']
    edit_form_extra_fields = {
        'wiki_entity_id': StringField('wiki_entity_id', widget=ReadOnlyField()),
        'imdb_id': StringField('imdb_id', widget=ReadOnlyField())
    }

    @action("muldelete", "Delete selected", "Delete all selected Really?", "fa-rocket", single=False)
    def muldelete(self, items):
        self.datamodel.delete_all(items)
        self.update_redirect()
        return redirect(self.get_redirect())
    
    @action("delete_all", "Delete all", f"Delete ALL movies Really?", "fa-rocket", single=False)
    def delete_all(self, items):
        try:
            db.session.query(Movie).delete()
            db.session.commit()
            flash("All items have been deleted.", "success")
        except Exception as e:
            db.session.rollback()
            flash("Failed to delete all items.", "error")
        return redirect(url_for("MovieView.list"))
    
    base_order = ('released_at', 'desc')

    # def get_query(self):
    #     query = super().get_query()
    #     query = query.add_columns(db.func.extract('year', Movie.released_at).label('released_at_year'))
    #     return query

    def get_group_by(self):
        group_by = super().get_group_by()
        group_by.append(db.func.extract('year', Movie.released_at))
        return group_by

db.create_all()


appbuilder.add_view(
    MovieView,
    "Movies",
    icon="fa-folder-open-o",
    category="My Category",
    category_icon='fa-envelope'
)

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )
