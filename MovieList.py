"""Class for MovieList - IMDb"""

import imdb
import pandas as pd


class MovieList:
    """"""

    def __init__(self, movies=None):
        """"""
        self.ia = imdb.Cinemagoer()
        self.movies = [] if movies is None else movies

    def get_top250_mov(self):
        """"""
        top = self.ia.get_top250_movies()
        self.movies = top
        top_250_movie_list = [[i + 1, top[i]['title'], top[i].movieID] for i in range(len(top))]
        df = pd.DataFrame(top_250_movie_list, columns=['Top', 'Movie Title', 'MovieID'])
        return df

    def get_bottom100_mov(self):
        """"""
        bottom = self.ia.get_bottom100_movies()
        self.movies = bottom
        top_250_movie_list = [[i + 1, bottom[i]['title'], bottom[i].movieID] for i in range(len(bottom))]
        df = pd.DataFrame(top_250_movie_list, columns=['Top', 'Movie Title', 'MovieID'])
        return df

    def get_pop100_mov(self):
        """"""
        top = self.ia.get_popular100_movies()
        self.movies = top
        top_250_movie_list = [[i + 1, top[i]['title'], top[i].movieID] for i in range(len(top))]
        df = pd.DataFrame(top_250_movie_list, columns=['Top', 'Movie Title', 'MovieID'])
        return df

    def get_pop100_tv(self):
        """"""
        top = self.ia.get_popular100_tv()
        self.movies = top
        top_250_movie_list = [[i + 1, top[i]['title'], top[i].movieID] for i in range(len(top))]
        df = pd.DataFrame(top_250_movie_list, columns=['Top', 'Series Title', 'MovieID'])
        return df

    def get_top50_genre_mov(self, genres=None):
        """"""
        genres = ["Drama"] if genres is None else genres
        top = self.ia.get_top50_movies_by_genres(genres=genres)
        self.movies = top
        top_250_movie_list = [[i + 1, top[i]['title'], top[i].movieID] for i in range(len(top))]
        df = pd.DataFrame(top_250_movie_list, columns=['Top', 'Movie Title', 'MovieID'])
        return df

    def get_top50_genre_tv(self, genres=None):
        """"""
        genres = ["Drama"] if genres is None else genres
        top = self.ia.get_top50_tv_by_genres(genres=genres)
        self.movies = top
        top_250_movie_list = [[i + 1, top[i]['title'], top[i].movieID] for i in range(len(top))]
        df = pd.DataFrame(top_250_movie_list, columns=['Top', 'Series Title', 'MovieID'])
        return df

    def get_top250_tv(self):
        """"""
        top = self.ia.get_top250_tv()
        self.movies = top
        top_250_movie_list = [[i + 1, top[i]['title'], top[i].movieID] for i in range(len(top))]
        df = pd.DataFrame(top_250_movie_list, columns=['Top', 'Series Title', 'MovieID'])
        return df

    def get_top250_ind_mov(self):
        """"""
        top = self.ia.get_top250_indian_movies()
        self.movies = top
        top_250_movie_list = [[i + 1, top[i]['title'], top[i].movieID] for i in range(len(top))]
        df = pd.DataFrame(top_250_movie_list, columns=['Top', 'Movie Title', 'MovieID'])
        return df
