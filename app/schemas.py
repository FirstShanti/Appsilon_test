from dataclasses import dataclass, asdict
import dateutil.parser

@dataclass
class WikiMovieSchema:
    imdb_id: str
    released_at: str
    title: str
    wiki_entity_id: str

    def __init__(self, imdb_id, released_at, title, wiki_entity_id):
        self.imdb_id = imdb_id.get('value')
        self.released_at = released_at.get('value')
        self.title = title.get('value')
        self.wiki_entity_id = wiki_entity_id.get('value')

    @property
    def to_dict(self):
        try:
            self.released_at = dateutil.parser.isoparse(self.released_at)
        except:
            self.released_at = None
        return {k: v for k, v in asdict(self).items()}