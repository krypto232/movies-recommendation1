from flask import Flask, render_template, request
import pickle
import requests
import os

app = Flask(__name__)

# -------------------------------
# Download similarity.pkl if not present
# -------------------------------
FILE_ID = "YOUR_FILE_ID_HERE"   # 👈 replace this
URL = f"https://drive.google.com/uc?id={FILE_ID}"
FILE_PATH = "similarity.pkl"

if not os.path.exists(FILE_PATH):
    print("Downloading similarity.pkl...")
    r = requests.get(URL)
    with open(FILE_PATH, "wb") as f:
        f.write(r.content)

# -------------------------------
# load data
# -------------------------------
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open(FILE_PATH, "rb"))

movie_list = movies['title'].values


# -------------------------------
# recommendation function
# -------------------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []

    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


# -------------------------------
# routes
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html", movie_list=movie_list)


@app.route("/recommend", methods=["POST"])
def get_recommendation():
    movie = request.form.get("movie")
    results = recommend(movie)

    return render_template(
        "index.html",
        movie_list=movie_list,
        recommendations=results
    )


# -------------------------------
# run app (IMPORTANT for Render)
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
