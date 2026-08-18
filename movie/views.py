import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import io
import base64
from collections import Counter
from django.shortcuts import render
from .models import Movie


def home(request):
    search_term = request.GET.get("searchMovie")

    if search_term:
        movies = Movie.objects.filter(title__icontains=search_term)
    else:
        movies = Movie.objects.all()

    return render(
        request,
        "home.html",
        {
            "name": "Isabela Ruiz de la Ossa",
            "searchTerm": search_term,
            "movies": movies,
        },
    )


def about(request):
    return render(request, "about.html")

def graph_to_base64(labels, values, title, xlabel):
    fig, ax = plt.subplots(figsize=(10, 5))

    positions = range(len(labels))
    ax.bar(positions, values)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Number of movies")

    ax.set_xticks(list(positions))
    ax.set_xticklabels(labels, rotation=90)

    fig.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)

    graphic = base64.b64encode(buffer.getvalue()).decode("utf-8")

    buffer.close()
    plt.close(fig)

    return graphic


def statistics_view(request):
    movies = Movie.objects.all()

    # Movies per year
    year_counts = Counter(
        movie.year for movie in movies if movie.year
    )

    years = sorted(year_counts.keys())

    graphic_year = graph_to_base64(
        years,
        [year_counts[year] for year in years],
        "Movies per year",
        "Year",
    )

    # Movies per genre: use ONLY the first genre
    first_genres = []

    for movie in movies:
        if movie.genre:
            first_genre = movie.genre.split(",")[0].strip()
            first_genres.append(first_genre)

    genre_counts = Counter(first_genres)
    genres = sorted(genre_counts.keys())

    graphic_genre = graph_to_base64(
        genres,
        [genre_counts[genre] for genre in genres],
        "Movies per genre",
        "Genre",
    )

    return render(
        request,
        "statistics.html",
        {
            "graphic_year": graphic_year,
            "graphic_genre": graphic_genre,
        },
    )