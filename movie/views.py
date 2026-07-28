from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(
        request,
        "home.html",
        {"name": "Isabela Ruiz de la Ossa"},
    )


def about(request):
    return render(request, "about.html")