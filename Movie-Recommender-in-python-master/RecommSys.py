# reccomemder system based on correlation

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.warn("ignore")

column_names = ['user_id', 'item_id', 'rating', 'timestamp'] #initializing the collumns
dataset = pd.read_csv('u.data',sep='\t',names = column_names)

movie_titles = pd.read_csv('Movie_Id_Titles') # movie names corresponding to their id's
dataset = pd.merge(dataset,movie_titles,on = 'item_id')

'''#taking the avg ratings
dataset.groupby('title')['rating'].mean().sort_values(ascending=False)

#sorting the ratings in the decsending order
dataset.groupby('title')['rating'].count().sort_values(ascending=False)
'''
# movie names with their avg ratings
ratings = pd.DataFrame(dataset.groupby('title')['rating'].mean())

# appending the num_of_ratings column in the rating
ratings['num_of_ratings'] = pd.DataFrame(dataset.groupby('title')['rating'].count())

# lets create a matrix which the info user's rating corresponding to the movie
moviemat = dataset.pivot_table(index = 'user_id',columns = 'title',values = 'rating')

#lets sort the ratings as Most rated movie
ratings = ratings.sort_values('num_of_ratings',ascending = False)

# let the genre of the starwars & liar liar be the scince fic & comedy
starwars_user_ratings = moviemat['Star Wars (1977)']
liarliar_user_ratings = moviemat['Liar Liar (1997)']

# We use corrwith() method to get correlations between two pandas series:
similar_to_starwars = moviemat.corrwith(starwars_user_ratings)

# remove that movies(contains rating nan) bcoz they are not watched
corr_starwars = pd.DataFrame(similar_to_starwars,columns= ['correlation'])
corr_starwars.dropna(inplace=True) #dropped nan

# by sorting the above table with correlation will gives the highes corelated movie with starwars
corr_starwars = corr_starwars.sort_values('correlation',ascending=False)

# joining the num_of_ratings from the ratings
corr_starwars = corr_starwars.join(ratings['num_of_ratings'])
# considering only those movies which have more than 100 reviews(took from the histogram)
corr_starwars = corr_starwars[corr_starwars['num_of_ratings']>100].sort_values('correlation',ascending=False)
print("Top 5 Recommendations : ")
print(corr_starwars.head(5))

# lets do the same for the liar liar movie
similar_to_liarliar = moviemat.corrwith(liarliar_user_ratings)

corr_liarliar = pd.DataFrame(similar_to_liarliar,columns=['correlation'])
corr_liarliar.dropna(inplace=True)

corr_liarliar = corr_liarliar.sort_values('correlation',ascending= False)
corr_liarliar = corr_liarliar.join(ratings['num_of_ratings'])
corr_liarliar = corr_liarliar[corr_liarliar['num_of_ratings']>100].sort_values('correlation',ascending=False)
print("Top 5 Recommendations : ")
print(corr_liarliar.head(5))