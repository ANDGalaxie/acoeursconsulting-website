from django.http import JsonResponse
from django.shortcuts import render


def page_context(current_nav=None):
    context = {}
    if current_nav:
        context["current_nav"] = current_nav
    return context


def home(request):
    return render(request, "website/home.html", page_context(current_nav="home"))


def enterprise_services(request):
    return render(
        request,
        "website/enterprise_services.html",
        page_context(current_nav="business"),
    )


def market_entry_service(request):
    return render(
        request,
        "website/service_market_entry.html",
        page_context(current_nav="business"),
    )


def company_banking_service(request):
    return render(
        request,
        "website/service_company_banking.html",
        page_context(current_nav="business"),
    )


def tax_legal_compliance_service(request):
    return render(
        request,
        "website/service_tax_legal_compliance.html",
        page_context(current_nav="business"),
    )


def local_operations_service(request):
    return render(
        request,
        "website/service_local_operations.html",
        page_context(current_nav="business"),
    )


def business_growth_service(request):
    return render(
        request,
        "website/service_business_growth.html",
        page_context(current_nav="business"),
    )


def personal_services(request):
    return render(
        request,
        "website/personal_services.html",
        page_context(current_nav="personal"),
    )


def residency_family_service(request):
    return render(
        request,
        "website/service_residency_family.html",
        page_context(current_nav="personal"),
    )


def property_wealth_service(request):
    return render(
        request,
        "website/service_property_wealth.html",
        page_context(current_nav="personal"),
    )


def cross_border_tax_risk_service(request):
    return render(
        request,
        "website/service_cross_border_tax_risk.html",
        page_context(current_nav="personal"),
    )


def about(request):
    return render(request, "website/about.html", page_context(current_nav="about"))


def legal_notice(request):
    return render(request, "website/legal_notice.html", page_context())


def privacy_policy(request):
    return render(request, "website/privacy_policy.html", page_context())


def cookie_policy(request):
    return render(request, "website/cookie_policy.html", page_context())


def placeholder(request, title, section):
    context = {
        "title": title,
        "section": section,
    }
    return render(request, "website/placeholder.html", context)


def health(request):
    return JsonResponse({"status": "ok"})
