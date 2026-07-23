from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("health/", views.health, name="health"),
    path(
        "business/",
        views.enterprise_services,
        name="business",
    ),
    path(
        "business/market-entry/",
        views.market_entry_service,
        name="business_market_entry",
    ),
    path(
        "business/company-banking/",
        views.company_banking_service,
        name="business_company_banking",
    ),
    path(
        "business/tax-legal-compliance/",
        views.tax_legal_compliance_service,
        name="business_tax_legal_compliance",
    ),
    path(
        "business/local-operations/",
        views.local_operations_service,
        name="business_local_operations",
    ),
    path(
        "business/growth/",
        views.business_growth_service,
        name="business_growth",
    ),
    path(
        "personal/",
        views.personal_services,
        name="personal",
    ),
    path(
        "personal/residency-family/",
        views.residency_family_service,
        name="personal_residency_family",
    ),
    path(
        "personal/property-wealth/",
        views.property_wealth_service,
        name="personal_property_wealth",
    ),
    path(
        "personal/cross-border-tax-risk/",
        views.cross_border_tax_risk_service,
        name="personal_cross_border_tax_risk",
    ),
    path(
        "about/",
        views.about,
        name="about",
    ),
    path(
        "contact/",
        views.contact,
        name="contact",
    ),
    path(
        "consultation/",
        views.consultation_redirect,
        name="consultation",
    ),
    path(
        "cases/listed-company-france/",
        views.case_study_redirect,
        name="case_listed_company_france",
    ),
    path(
        "legal/",
        views.legal_notice,
        name="legal",
    ),
    path(
        "privacy/",
        views.privacy_policy,
        name="privacy",
    ),
    path(
        "cookies/",
        views.cookie_policy,
        name="cookies",
    ),
    path(
        "fr/",
        views.placeholder,
        {"title": "Version francaise", "section": "语言版本预留"},
        name="fr",
    ),
    path(
        "en/",
        views.placeholder,
        {"title": "English Version", "section": "语言版本预留"},
        name="en",
    ),
]
