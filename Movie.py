"""Class for Movie - IMDb"""

import pandas as pd
import numpy as np
import imdb
import re
from textblob import TextBlob
import nltk
import text2emotion as te


class Movie:
    """Movie from IMDb"""
    def __init__(self, movie_id=None):
        """"""
        self.ia = imdb.Cinemagoer()
        self.movie_id = movie_id if not None else '0111161'
        self.info = self.get_movie_info()
        # self.genres = self.get_genres()
        # self.languages = self.get_languages()
        # self.plot = self.get_plot()
        # self.year = self.get_year()
        # self.actors = self.get_actors()
        # self.directors = self.get_directors()
        # self.rating = self.get_rating()
        # self.reviews = self.get_reviews()
        # self.cleaned_reviews = self.cleaned_review_text()
        # self.subjectivity_data = self.get_subjectivity_data()
        # self.subjectivity = self.get_subjectivity()
        # self.polarity_data = self.get_polarity_data()
        # self.polarity = self.get_polarity()
        # self.sentiment_data = self.get_sentiment_data()
        # self.common_sentiment = self.common_sentiment()
        # self.emotion_data = self.get_emotion_data()
        # self.emotion_scale = self.get_emotion_scale()
        # self.movie_review_df = self.get_movie_review_df()
        # self.movie_row = self.get_movie_row()
        # self.movie_name_id_row = self.get_movie_name_id_row()
        # self.movie_sent_emo_row = self.get_movie_sent_emo_row()

    def get_movie_info(self):
        """Dictionary with all movie information"""
        get_info = self.ia.get_movie_main(self.movie_id)['data']
        return get_info

    def get_genres(self):
        """String with genres"""
        genre_list = self.info['genres']
        genres = ', '.join([genre_list[i] for i in range(len(genre_list))])
        return genres

    def get_languages(self):
        """String with languages"""
        language_list = self.info['languages']
        languages = ', '.join([language_list[i] for i in range(len(language_list))])
        return languages

    def get_plot(self):
        """String with plot"""
        try:
            return self.info['plot outline']
        except KeyError:
            return pd.NA

    def get_year(self):
        """Year as integer"""
        try:
            return self.info['year']
        except KeyError:
            return pd.NA

    def get_actors(self):
        """String with actors"""
        try:
            actor_list = self.info['cast']
        except KeyError:
            return pd.NA
        range_actor = 5 if len(actor_list) > 4 else len(actor_list)
        actors = ', '.join([actor_list[i]['name'] for i in range(range_actor)])
        return actors

    def get_directors(self):
        """String with directors"""
        director_list = self.info['director']
        directors = ', '.join([director_list[i]['name'] for i in range(len(director_list))])
        return directors

    def get_rating(self):
        """IMDb rating as float/integer"""
        try:
            return self.info['rating']
        except KeyError:
            return pd.NA

    def get_movie_row(self):
        """List with movie rating, year, languages, genres, plot, directors, actors"""
        return [self.get_rating(), self.get_year(), self.get_languages(), self.get_genres(), self.get_plot(),
                self.get_directors(), self.get_actors()]

    def get_movie_name_id_row(self):
        """List with movie title, IMDb movieID"""
        return [self.info['title'], self.movie_id]

    def get_movie_sent_emo_row(self):
        """"""
        return [self.get_subjectivity(), self.get_polarity(), self.common_sentiment(), self.get_emotion_scale()]

    def get_reviews(self):
        """Dataframe with IMDb user movie Reviews"""
        try:
            get_movie_reviews = self.ia.get_movie_reviews(self.movie_id)['data']['reviews']
            review_list = []
            for review in get_movie_reviews:
                review_list.append([review['rating'], review['title'], review['content']])
            df = pd.DataFrame(review_list, columns=['Rating', 'Review Title', 'Review'])
            return df
        except KeyError:
            return pd.DataFrame([[pd.NA, pd.NA, pd.NA]]*25, columns=['Rating', 'Review Title', 'Review'])

    def cleaned_review_text(self):
        """Dataframe with Cleaned Reviews"""
        stopwords = ["for", "on", "an", "a", "of", "and", "in", "the", "to", "from"]
        df = self.get_reviews()
        df_ct = pd.Series()
        df_cr = pd.Series()
        dfc = pd.DataFrame(columns=['Cleaned Review Title', 'Cleaned Review'])
        for i in ['Review Title', 'Review']:
            count = 0
            for text in df[f'{i}']:
                if type(text) is float or type(text) is int or text is pd.NA:
                    temp = ""
                else:
                    temp = text.lower()
                    temp = re.sub("'", "", temp)  # to avoid removing contractions in english
                    temp = re.sub("@[A-Za-z0-9_]+", "", temp)
                    temp = re.sub("#[A-Za-z0-9_]+", "", temp)
                    temp = re.sub(r'http\S+', '', temp)
                    temp = re.sub('[()!?]', ' ', temp)
                    temp = re.sub('\[.*?\]', ' ', temp)
                    temp = re.sub("[^a-z0-9]", " ", temp)
                    temp = temp.split()
                    temp = [w for w in temp if not w in stopwords]
                    temp = " ".join(word for word in temp)
                if i == 'Review':
                    df_cr.loc[count] = temp
                else:
                    df_ct.loc[count] = temp
                count += 1
        dfc['Cleaned Review Title'], dfc['Cleaned Review'] = df_ct, df_cr
        return dfc

    def get_subjectivity_data(self):
        """Dataframe with Subjectivity for each review"""
        cr = self.cleaned_review_text()
        dft = pd.DataFrame()
        dft['TR Combo'] = cr['Cleaned Review Title'] + ' ' + cr['Cleaned Review']
        se = pd.Series()
        dfs = pd.DataFrame(columns=['Subjectivity'])
        count = 0
        for text in dft['TR Combo']:
            blob = TextBlob(text)
            subj = blob.sentiment.subjectivity
            se.loc[count] = subj
            count += 1
        dfs['Subjectivity'] = se
        return dfs

    def get_polarity_data(self):
        """Dataframe with Polarity for each review"""
        cr = self.cleaned_review_text()
        dft = pd.DataFrame()
        dft['TR Combo'] = cr['Cleaned Review Title'] + ' ' + cr['Cleaned Review']
        se = pd.Series()
        dfs = pd.DataFrame(columns=['Polarity'])
        count = 0
        for text in dft['TR Combo']:
            blob = TextBlob(text)
            subj = blob.sentiment.polarity
            se.loc[count] = subj
            count += 1
        dfs['Polarity'] = se
        return dfs

    def get_sentiment_data(self):
        """Dataframe with sentiment for each review"""
        dfp = self.get_polarity_data()
        se = pd.Series()
        dfs = pd.DataFrame(columns=['Sentiment'])
        count = 0
        for score in dfp['Polarity']:
            if score < 0:
                sentiment = 'Negative'
            elif score == 0:
                sentiment = 'Neutral'
            else:
                sentiment = 'Positive'
            se.loc[count] = sentiment
            count += 1
        dfs['Sentiment'] = se
        return dfs

    def get_subjectivity(self):
        """Float with average subjectivity for movie"""
        return self.get_subjectivity_data()['Subjectivity'].mean()

    def get_polarity(self):
        """Float for average polarity for movie"""
        return self.get_polarity_data()['Polarity'].mean()

    def common_sentiment(self):
        """String for mode of sentiments from movie reviews"""
        return self.get_sentiment_data()['Sentiment'].mode()[0]

    def get_emotion_data(self):
        """Dataframe with emotion scale from each movie review"""
        df = self.cleaned_review_text()
        dfe = pd.DataFrame()
        dfe['Emotion Scale'] = (df['Cleaned Review Title'] + ' ' + df['Cleaned Review']).apply(te.get_emotion)
        return dfe

    def get_emotion_scale(self):
        """Dictionary for average emotion scale for movie"""
        df = self.get_emotion_data()
        base_dict = {k: 0 for k in df['Emotion Scale'][0]}
        for i in df['Emotion Scale']:
            for k in i:
                base_dict[k] += i[k]
        tot_emo_dict = {k: round(base_dict[k] / df['Emotion Scale'].count(), 4) for k in base_dict}
        return tot_emo_dict

    def get_movie_review_df(self):
        """Dataframe for movie reviews analysis"""
        df1 = self.get_reviews()
        df = df1.join(self.cleaned_review_text()).join(self.get_subjectivity_data()).join(self.get_polarity_data()).join(
            self.get_sentiment_data()).join(self.get_emotion_data())
        return df

