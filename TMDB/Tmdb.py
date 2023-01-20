import requests
import imdb
import config


def get_movie_imdb_id(title):
    ia = imdb.Cinemagoer()
    movies = ia.search_movie_advanced(title)
    return movies[0]['title'], movies[0].movieID


class TmdbDownloader:

    def __init__(self):
        self.KEY = config.KEY

    def __size_str_to_int__(self, x):
        return float("inf") if x == 'original' else int(x[1:])

    def __get_image_config__(self):

        CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'

        url = CONFIG_PATTERN.format(key=self.KEY)
        r = requests.get(url)
        config = r.json()
        base_url = config["images"]["base_url"]
        poster_sizes = config["images"]["poster_sizes"]
        max_size = max(poster_sizes, key=self.__size_str_to_int__)
        return base_url, max_size

    def get_image(self, title):
        filename, movie_id = get_movie_imdb_id(title)
        if movie_id == "null":
            print("there is no such movie")
        else:
            # get the movie information json file
            IMG_PATTERN = 'http://api.themoviedb.org/3/movie/tt{imdb_id}/images?api_key={key}'
            r = requests.get(IMG_PATTERN.format(key=self.KEY, imdb_id=movie_id))
            api_response = r.json()
            poster = api_response['posters'][0]

            # get the poster for the movie with the requested size
            (base_url, max_size) = self.__get_image_config__()
            rel_path = poster['file_path']
            url = "{0}{1}{2}".format(base_url, max_size, rel_path)
            r = requests.get(url)
            filetype = r.headers['content-type'].split('/')[-1]
            return r.content, filename, movie_id, filetype




