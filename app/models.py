from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint


class Movie(Model):
    id = Column(Integer, primary_key=True)
    imdb_id = Column(String(32))

    wiki_entity_id = Column(String(32), nullable=False)
    title = Column(String(256), nullable=False)
    released_at = Column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint('imdb_id', 'wiki_entity_id', name='wiki_imdb_ids'),
    )

    def __repr__(self):
        return self.title


MovieModelInterface = SQLAInterface(Movie)
