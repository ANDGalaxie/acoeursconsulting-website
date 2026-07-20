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


def market_entry_service(request):
    context = {
        "canonical_url": request.build_absolute_uri(request.path),
        "current_nav": "business",
    }
    return render(request, "website/service_market_entry.html", context)


def company_banking_service(request):
    context = {
        "canonical_url": request.build_absolute_uri(request.path),
        "current_nav": "business",
    }
    return render(request, "website/service_company_banking.html", context)


def tax_legal_compliance_service(request):
    context = {
        "canonical_url": request.build_absolute_uri(request.path),
        "current_nav": "business",
    }
    return render(request, "website/service_tax_legal_compliance.html", context)


def local_operations_service(request):
    context = {
        "canonical_url": request.build_absolute_uri(request.path),
        "current_nav": "business",
    }
    return render(request, "website/service_local_operations.html", context)


def business_growth_service(request):
    context = {
        "canonical_url": request.build_absolute_uri(request.path),
        "current_nav": "business",
    }
    return render(request, "website/service_business_growth.html", context)


def placeholder(request, title, section):
    context = {
        "title": title,
        "section": section,
    }
    return render(request, "website/placeholder.html", context)


def health(request):
    return JsonResponse({"status": "ok"})
