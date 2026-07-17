from django.shortcuts import render


def home(request):
    return render(request, "website/home.html")


def placeholder(request, title, section):
    context = {
        "title": title,
        "section": section,
    }
    return render(request, "website/placeholder.html", context)
