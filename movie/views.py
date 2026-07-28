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
            "name": "Isabella Hernández Posada",
            "searchTerm": search_term,
            "movies": movies,
        },
    )


def about(request):
    return render(request, "about.html")