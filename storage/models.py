class Movie:
    """
    Represents a movie in the database
    """
    
    def __init__(
        self,
        id: int,
        title: str,
        original_title: str = None,
        overview: str = None,
        popularity: float = None,
        vote_average: float = None,
        vote_count: int = None,
        release_date: str = None,
        release_year: int = None,
        genres: str = None,
        adult: bool = False,
        poster_path: str = None,
        backdrop_path: str = None,
        original_language: str = None,
        weighted_rating: float = None
    ):
        self.id = id
        self.title = title
        self.original_title = original_title
        self.overview = overview
        self.popularity = popularity
        self.vote_average = vote_average
        self.vote_count = vote_count
        self.release_date = release_date
        self.release_year = release_year
        self.genres = genres
        self.adult = adult
        self.poster_path = poster_path
        self.backdrop_path = backdrop_path
        self.original_language = original_language
        self.weighted_rating = weighted_rating
    
    def __repr__(self):
        return f"<Movie {self.id}: {self.title}>"


class Genre:
    """
    Represents a movie genre
    """
    
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return f"<Genre {self.id}: {self.name}>"
