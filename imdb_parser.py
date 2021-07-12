import random
import re
import requests
from bs4 import BeautifulSoup

TOP_250_MOVIES_LIST = "https://www.imdb.com/chart/top"
TOP_250_SERIES_LIST = "https://www.imdb.com/chart/toptv"


def get_movie() -> dict:
    movie = choose_randomly(TOP_250_MOVIES_LIST)
    additional_info = get_info(movie["url"])

    return {
        "title": movie["title"],
        "year": movie["year"],
        "poster": movie["poster"],
        "rating": movie["rating"],
        "description": additional_info["description"],
        "genre": additional_info["genre"],
        "duration": additional_info["duration"],
    }


def get_series() -> dict:
    series = choose_randomly(TOP_250_SERIES_LIST)
    additional_info = get_info(series["url"])

    return {
        "title": series["title"],
        "year": series["year"],
        "poster": series["poster"],
        "rating": series["rating"],
        "description": additional_info["description"],
        "genre": additional_info["genre"],
    }


def choose_randomly(url) -> dict:
    page = BeautifulSoup(
        requests.get(url).text,
        "lxml"
    )

    movies_on_page = page.find_all(class_="titleColumn")
    random_movie = movies_on_page[random.randrange(0, 250)]

    # Retrieving a poster's url. We need to strip (or cut) some substring from there
    poster_full_url = random_movie.parent.find(class_="posterColumn").a.img["src"]
    poster_stripped = re.sub(r"\._.+(.jpg$)", r"\g<1>", poster_full_url)

    return {
        "url": "https://www.imdb.com" + random_movie.a["href"],
        "title": random_movie.a.string,
        "year": random_movie.span.string[1:5],
        "poster": poster_stripped,
        "rating": random_movie.parent.find(class_="imdbRating").strong.string,
    }


def get_info(movie_url) -> dict:
    movie_page = BeautifulSoup(
        requests.get(movie_url).text,
        "lxml"
    )

    desc = movie_page.find(class_=re.compile(r"^GenresAndPlot__TextContainerBreakpointXL")).string

    genres = []
    for genre in movie_page.find_all(class_=re.compile(r"^GenresAndPlot__GenreChip")):
        genres.append(genre.span.string)

    duration = ""
    metadata = movie_page.find(class_=re.compile("^TitleBlock__TitleMetaDataContainer")).find("li")
    if metadata:
        duration = metadata.find_next_sibling("li").find_next_sibling("li").string

    return {
        "description": desc,
        "genre": ", ".join(genres),
        "duration": duration,
    }
