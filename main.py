import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from io import StringIO

df = pd.read_csv("movies_metadata.csv", dtype=str)
#initial filter on original_language and genres
df = df.loc[(df["original_language"] == "en") & (df["genres"] != "[]")]
#build new columns and filter on year_of_release
df["budget"] = pd.to_numeric(df["budget"])
df["revenue"] = pd.to_numeric(df["revenue"])
df["profit"] = df["revenue"] - df["budget"]
df["year_of_release"] = pd.to_datetime(df["release_date"], format="%Y-%m-%d").dt.strftime('%Y').apply(pd.to_numeric)
df = df.loc[(df["year_of_release"] >= 1970) & (df["year_of_release"] < 2017)]

#add columns for each genre category
def split_values(row):
    for old, new in replacements:
        row = re.sub(old, new, row)
    values = row.split('?')
    values = values[1::2]
    return values

def get_genre_true_false(row,value):
    values = split_values(row)
    if value in values:
        return True
    else:
        return False

replacements = [
    ("TV Movie", "Tvmovie"),
    ("Science Fiction", "Sciencefiction"),
    (r"([A-Z])",r" ?\1"),
    ('}', '?'),
    ("'", "")
]

unique_genres = []
rows = df["genres"].unique().tolist()
for row in rows:
    splitted_genres = split_values(row)
    for genre in splitted_genres:
        if genre not in unique_genres:
            unique_genres.append(genre)

for genre in unique_genres:
    df[genre] = df["genres"].apply(get_genre_true_false, value=genre)

#get high grossing movies
release_years = list(set(df["year_of_release"]))
df_high_grossing = df.loc[df["profit"] > 100000000]
high_grossing_movies_by_year = []
for year in release_years:
    rows = df_high_grossing.loc[df_high_grossing["year_of_release"] == year]
    high_grossing_movies_by_year.append(len(rows["title"].tolist()))

fig = plt.figure()
plt.plot(release_years, high_grossing_movies_by_year)
plt.xlabel("Release Year")
plt.ylabel("Number of Movies Grossing > 100M")
plt.grid(True)
fig.savefig('static/images/high_grossing_movies_per_year_high.png', dpi=fig.dpi)
plt.show()

genre_list = []
for genre in unique_genres:
    df_high_grossing_genre = df_high_grossing.loc[df_high_grossing[genre] == True][["title", "profit"]].values.tolist()
    genre_list.append(df_high_grossing_genre)
movies_per_genre = [len(i) for i in genre_list]


fig = plt.figure()
fig.set_size_inches(12.5, 10.5)
plt.plot(unique_genres, movies_per_genre)
plt.xlabel("Genre")
plt.xticks(rotation=90)
plt.ylabel("Movies")
plt.grid(True)
fig.savefig('static/images/movies_per_genre.png', dpi=fig.dpi)
plt.show()

df_high_grossing_sorted = df_high_grossing.sort_values("profit", ascending=False)
print(df_high_grossing_sorted[["title", "year_of_release", "profit"]].head(10))

df_high_grossing_belongs_to_collection = df_high_grossing.dropna(subset=["belongs_to_collection"])

high_grossing_movies_in_collections_by_year = []
for year in release_years:
    rows = df_high_grossing_belongs_to_collection.loc[df_high_grossing_belongs_to_collection["year_of_release"] == year]
    high_grossing_movies_in_collections_by_year.append(len(rows["title"].tolist()))

fig = plt.figure()
plt.plot(release_years, high_grossing_movies_by_year, label="No. High Grossing Movies")
plt.plot(release_years, high_grossing_movies_in_collections_by_year, label="No. High Grossing Movies in Franchise")
plt.xlabel("Release Year")
plt.ylabel("Number of Movies Grossing > 500M")
plt.grid(True)
plt.legend()
fig.savefig('static/images/movies_in_collections_per_year_500.png', dpi=fig.dpi)
plt.show()

x = np.array(release_years).reshape((-1,1))
y = np.array(high_grossing_movies_by_year)

#linear regression on high_grossing_movies_by_year
model = LinearRegression().fit(x,y)
r_sq = model.score(x,y)
slope = model.coef_
intercept = model.intercept_
print(f"Line equation: {slope}X + {intercept}")
print(f"R-Squared Coefficient: {r_sq}")
y_values = [i*slope + intercept for i in release_years]

fig = plt.figure()
plt.plot(release_years, high_grossing_movies_by_year)
plt.plot(release_years, y_values)
plt.xlabel("Release Year")
plt.ylabel("Number of Movies Grossing > 100M")
plt.grid(True)
fig.savefig('static/images/linear_regression_high.png', dpi=fig.dpi)
plt.show()

#polynomial regression
transformer = PolynomialFeatures(degree=2, include_bias=False)
x_ = transformer.fit_transform(x)
model = LinearRegression().fit(x_,y)
y_pred = model.predict(x_)
r_sq = model.score(x_,y)
slope = model.coef_
intercept = model.intercept_
print(f"Line equation: {slope[1]}X^2 {slope[0]}X + {intercept}")
print(f"R-Squared Coefficient: {r_sq}")

fig = plt.figure()
plt.plot(x, y_pred)
plt.plot(release_years, high_grossing_movies_by_year)
plt.xlabel("Release Year")
plt.ylabel("Number of Movies Grossing > 100M")
plt.grid(True)
fig.savefig('static/images/polynomial_regression_high.png', dpi=fig.dpi)
plt.show()