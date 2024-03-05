import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

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

def check_null(value):
    if pd.isna(value):
        return "No"
    else:
        return "Yes"

def change_units(value):
    return round(value / 100000000, 3)

def float_to_int(value):
    return int(value)

df = pd.read_csv("movies_metadata.csv", dtype=str)
df = df.loc[(df["original_language"] == "en") & (df["genres"] != "[]")]

df["budget"] = pd.to_numeric(df["budget"])
df["revenue"] = pd.to_numeric(df["revenue"])
df["profit"] = df["revenue"] - df["budget"]
df["year_of_release"] = pd.to_datetime(df["release_date"], format="%Y-%m-%d").dt.strftime('%Y').apply(pd.to_numeric)
df = df.loc[(df["year_of_release"] >= 1970) & (df["year_of_release"] < 2017)]

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

release_years = list(set(df["year_of_release"]))
df_high_grossing = df.loc[df["profit"] > 100000000]
high_grossing_movies_by_year = []
for year in release_years:
    rows = df_high_grossing.loc[df_high_grossing["year_of_release"] == year]
    high_grossing_movies_by_year.append(len(rows["title"].tolist()))

df_high_grossing_sorted = df_high_grossing.sort_values("profit", ascending=False)
df_high_grossing_sorted["in a franchise"] = df_high_grossing["belongs_to_collection"].apply(check_null)
df_high_grossing_sorted["profit in units of 100M"] = df_high_grossing["profit"].apply(change_units)
df_high_grossing_sorted["release year"] = df_high_grossing_sorted["year_of_release"].apply(float_to_int)
df_high_grossing_sorted[["title","profit in units of 100M","in a franchise","release year"]].head(20).to_csv("high_grossing_movies.csv", index=False)

df_high_grossing_belongs_to_collection = df_high_grossing.dropna(subset=["belongs_to_collection"])

high_grossing_movies_in_collections_by_year = []
for year in release_years:
    rows = df_high_grossing_belongs_to_collection.loc[df_high_grossing_belongs_to_collection["year_of_release"] == year]
    high_grossing_movies_in_collections_by_year.append(len(rows["title"].tolist()))

fig = plt.figure()
plt.plot(release_years, high_grossing_movies_by_year, label="No. High Grossing Movies")
plt.plot(release_years, high_grossing_movies_in_collections_by_year, label="No. High Grossing Movies in Franchise")
plt.xlabel("Release Year")
plt.ylabel("Number of Movies Grossing > 100M")
plt.grid(True)
plt.legend()
fig.savefig('static/images/movies_in_collections_per_year_100m.png', dpi=fig.dpi)
plt.show()

x = np.array(release_years).reshape((-1,1))
y = np.array(high_grossing_movies_by_year)

y_dict = {"Movies": high_grossing_movies_by_year, "Movies in Franchise": high_grossing_movies_in_collections_by_year}

fig = plt.figure(figsize=(8,8))
count = 1
for key, values in y_dict.items():
    y = np.array(values)
    transformer = PolynomialFeatures(degree=2, include_bias=False)
    x_ = transformer.fit_transform(x)
    model = LinearRegression().fit(x_,y)
    y_pred = model.predict(x_)
    r_sq = model.score(x_,y)
    slope = model.coef_
    intercept = model.intercept_
    print(f"Line equation: {slope[1]}X^2 {slope[0]}X + {intercept}")
    print(f"R-Squared Coefficient: {r_sq}")
    ax = fig.add_subplot(2,1,count)
    ax.plot(x, y_pred)
    ax.plot(release_years, values)
    ax.annotate(f"R^2: {r_sq}", xy=(1970,75-(count*25)))
    ax.set_xlabel("Release Year")
    ax.set_ylabel(f"No. {key} Grossing > 100M")
    count += 1

fig.savefig(f'static/images/polynomial_regression_100m.png', dpi=fig.dpi)
plt.show()