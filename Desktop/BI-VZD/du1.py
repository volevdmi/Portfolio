#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time 
import pandas as pd
import numpy as np
import math
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib_inline
import seaborn as sns
import matplotlib.pyplot as plt

def print_df(data):
    print(data)

def info(data):
    print(data.info())


def get_genres(data):
    genre_list = []
    for i in data['genres']:
        i = i.replace('[', '')
        i = i.replace(']', '')
        i = i.replace('\'', '')
        i = i.replace(', ', '|')
        i = i.split("|")
        j = len(i)-1
        while(j!=-1):
            if(i[j] not in genre_list):
                genre_list.append(i[j])
                    #print(i[j])                    
                j-=1
    return genre_list
    

def delete_zero_genre(data):
    return data.loc[data['genres'] != '[]']
    
def delete_zero_popularity(data):
    return data.loc[data['popularity'] >= 20]


def delete_nan_values(data):
    return data.dropna()

def delete_low_follower(data):
    return data.loc[data['followers'] >= 100000]



def row_by_id(data, column, index):
    return data.loc[index, column]

def max_value_index(column, data):
    index = data[column].idxmax()
    return index

def plot_followers_popularity(data):
    #sns.lineplot(x='followers', y='popularity', data = data)
    #sns.histplot(x = "followers", y = "popularity", data = data)
    #plt.plot(data['popularity'], data['followers'])
    plt.scatter(data['popularity'], data['followers'], s = 1, )
    fig, ax = plt.subplots()
    data['popularity'].hist(bins = 100)
    ax.set_xlabel('popularity')
    plt.show()

def median(data, column):
    return np.median(data[column])

def add_outcome(data, median_popularity, median_followers):
    data['outcome'] = 0
    data['outcome'] = np.where(((data['popularity'] >= median_popularity) & (data['followers'] >= median_followers)), 1, data.outcome)
    return data
    


def decision_tree(data):
    data.drop(columns = ['id', 'name', 'genres'], axis = 1, inplace=True)
    feature_cols = list(data.columns)
    X = data
    y = data['outcome']
    X_train, X_test, y_train, y_test = train_test_split(X[feature_cols],
                                                        y, test_size=0.3, 
                                                        random_state=42, 
                                                        stratify=y
                                                        )    
    
    clf = DecisionTreeClassifier(max_depth=5)
    clf = clf.fit(X_train, y_train)
    y_pred_train = clf.predict(X_train)
    print('Train Accuracy: ', metrics.accuracy_score(y_train, y_pred_train))   


def main():
    ''' id | followers | genres | name | popularity '''
    
    df_artists = pd.read_csv('C:/Users/acer/Desktop/BI-VZD/artists.csv', sep = ',')
    
    print("Artists dataframe looks like: \n")
    print_df(df_artists.head(5))
    info(df_artists)
    print("\n\n\n")
    print("Amount Artists before droping: " + str(len(df_artists)))    
    df_artists = delete_nan_values(df_artists)
    
    print("Let's delete all artists, which popularity less than 20")
    df_artists = delete_zero_popularity(df_artists)
   
    
    print("Let's delete all artists, which don't have a genre")
    df_artists = delete_zero_genre(df_artists)
    print("Amount Artists after droping: " + str(len(df_artists))) 
    
    #genres = get_genres(df_artists)
    #print("There are " + str(len(genres)) + " different genres\n")    
    
    
    max_popularity_index = max_value_index("popularity", df_artists)
    max_followers_index = max_value_index("followers", df_artists)
    max_popularity_name = row_by_id(df_artists, 'name', max_popularity_index)
    max_popularity_value = row_by_id(df_artists, 'popularity', max_popularity_index)
    print(str(max_popularity_name) + " has the biggest popularity: " + str(max_popularity_value))
    max_followers_name =  row_by_id(df_artists, 'name', max_followers_index)
    max_followers_value =  row_by_id(df_artists, 'followers', max_followers_index)
    print(str(max_followers_name) + " has the biggest amount of followers: " + str(max_followers_value))
    
    print("Let's delete artists, who has less than 100.000 followers")
    df_artists = delete_low_follower(df_artists)
   
    plot_followers_popularity(df_artists)
    
    median_popularity = median(df_artists, 'popularity')
    median_followers= median(df_artists, 'followers')
    
    df_artists = add_outcome(df_artists, median_popularity, median_followers)
    df_artists.to_csv("new.csv")
    
    decision_tree(df_artists)

main()

