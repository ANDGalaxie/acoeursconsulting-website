from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, "website/home.html", {"current_nav": "home"})


def enterprise_services(request):
    context = {
        "canonical_url": request.build_absolute_uri(request.path),
        "current_nav": "business",
    }
    return render(request, "website/enterprise_services.html", context)


def placeholder(request, title, section):
    context = {
        "title": title,
        "section": section,
    }
    return render(request, "website/placeholder.html", context)


def health(request):
    return JsonResponse({"status": "ok"})
