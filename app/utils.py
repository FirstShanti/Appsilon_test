import sys
import logging
from SPARQLWrapper import SPARQLWrapper, JSON

from app import logging
from app.schemas import WikiMovieSchema
from app.models import Movie
from sqlalchemy.dialects.postgresql import insert


loger = logging.getLogger(__name__)
loger.setLevel(logging.INFO)


def create_update_data(db=None):

    endpoint_url = "https://query.wikidata.org/sparql"

    query = """
        SELECT DISTINCT ?wiki_entity_id ?title ?imdb_id ?released_at
        WHERE {
            ?movie wdt:P31 wd:Q11424;  # Instance of film
                    wdt:P577 ?released_at;  # Release date
                    wdt:P345 ?imdb_id;  # IMDb ID
                    rdfs:label ?title.
            
            FILTER (YEAR(?released_at) > 2013)
            FILTER (?released_at <= now())  # Filter only released films
            FILTER (LANG(?title) = "en")
            
            FILTER NOT EXISTS {
                ?other_wiki_entity_id wdt:P31 wd:Q11424;
                            wdt:P577 ?otherReleaseDate;
                            wdt:P345 ?imdb_id;
                            rdfs:label ?otherTitle.
                FILTER (YEAR(?otherReleaseDate) > 2013)
                FILTER (?otherReleaseDate <= now())
                FILTER (LANG(?otherTitle) = "en")
                FILTER (?otherReleaseDate < ?released_at)
            }

            BIND(strafter(str(?movie), "entity/") AS ?wiki_entity_id)
            
        }
    """

    def get_data(endpoint_url, query):
        loger.info(f'Request data from {endpoint_url}')
        try:
            user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
            sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            loger.info('Data successfully retrieved!')
            return sparql.query().convert().get('results', {}).get('bindings', [])
        except Exception as e:
            loger.error('Request error: ', e)
            return {}

    result = get_data(endpoint_url, query)

    wiki_movies = (WikiMovieSchema(**movie_data).to_dict for movie_data in result)

    loger.info(f'Begin storing the retrieved movies({len(result)}) in the database.')

    statement = insert(Movie).values(list(wiki_movies))

    statement = statement.on_conflict_do_nothing(index_elements=['imdb_id', 'wiki_entity_id'])

    db.session.execute(statement)
    db.session.commit()
