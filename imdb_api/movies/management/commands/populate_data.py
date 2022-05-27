from django_seed import Seed
from django.core.management.base import BaseCommand
from imdb_api.movies.models import Movie
from imdb_api.movies.constants import MOVIE_GENRES

seeder = Seed.seeder()

class Command(BaseCommand):
    def populate_movies(self):

            seeder.add_entity(
                Movie, 15, {
                    'title': lambda x: seeder.faker.sentence(nb_words=4),
                    'description': lambda x: seeder.faker.paragraph(nb_sentences=8),
                    'cover_image_url': 'https://picsum.photos/200/300',
                    'genre': lambda x: seeder.faker.random_element(elements=[x[0] for x in MOVIE_GENRES]),
                    
                })

            seeder.execute()

    def handle(self, **options):
        self.populate_movies()

