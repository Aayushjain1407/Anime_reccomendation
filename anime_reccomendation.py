# -*- coding: utf-8 -*-
"""anime_reccomendation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1z-QD9BKapSnn8fmAjOU4dfTaoWPWud8V
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
from google.colab import files
uploaded = files.upload()

#merging two datasets
df = pd.read_csv('rating.csv')
anime = pd.read_csv('anime.csv')
df = pd.merge(df,anime.drop('rating',axis=1),on='anime_id')
df.head()

# Top 10 Anime (sorted by rating)
df.groupby('name')['rating'].mean().sort_values(ascending=False).head(10)

#Top 10 Anime (sorted by watching)
df.groupby('name')['rating'].count().sort_values(ascending=False).head(10)

#data analysis
ratings = pd.DataFrame(df.groupby('name')['rating'].mean())
ratings['num of ratings'] = pd.DataFrame(df.groupby('name')['rating'].count())

genre_dict = pd.DataFrame(data=anime[['name','genre']])
genre_dict.set_index('name',inplace=True)
ratings.head()

#plot
plt.figure(figsize=(15,5))
ratings['num of ratings'].hist(bins=300)
plt.xlim(-10,3000)

#histogram
ratings['rating'].hist(bins=50)

sns.jointplot(x='rating',y='num of ratings',data=ratings)

#creating functions to check the genre of anime and to return reccomendation
def check_genre(genre_list,string):
    if any(x in string for x in genre_list):
        return True
    else:
        return False

def get_recommendation(name):
    #generating list of anime with the same genre with target
    anime_genre = genre_dict.loc[name].values[0].split(', ')
    cols = anime[anime['genre'].apply(
        lambda x: check_genre(anime_genre,str(x)))]['name'].tolist()

    #create matrix based on generated list
    animemat = df[df['name'].isin(cols)].pivot_table(
        index='user_id',columns='name',values='rating')

    #create correlation table
    anime_user_rating = animemat[name]
    similiar_anime = animemat.corrwith(anime_user_rating)
    corr_anime = pd.DataFrame(similiar_anime,columns=['correlation'])
    corr_anime = corr_anime.join(ratings['num of ratings'])
    corr_anime.dropna(inplace=True)
    corr_anime = corr_anime[corr_anime['num of ratings']>100].sort_values(
        'correlation',ascending=False)

    return corr_anime.head(10)

#testing
get_recommendation('Hunter x Hunter (2011)')

#testing
get_recommendation('Rainbow: Nisha Rokubou no Shichinin')

get_recommendation('Wake Up! Aria: Majokko Virgin Kiki Ippatsu')