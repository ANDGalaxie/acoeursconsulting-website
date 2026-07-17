from django.test import TestCase
from django.urls import reverse


class WebsiteRouteTests(TestCase):
    placeholder_routes = [
        "business",
        "business_market_entry",
        "business_company_banking",
        "business_tax_legal_compliance",
        "business_local_operations",
        "business_growth",
        "personal",
        "personal_residency_family",
        "personal_property_wealth",
        "personal_cross_border_tax_risk",
        "about",
        "consultation",
        "case_listed_company_france",
        "legal",
        "privacy",
        "cookies",
        "fr",
        "en",
    ]

    def test_homepage_returns_http_200(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

    def test_homepage_uses_expected_template(self):
        response = self.client.get(reverse("home"))

        self.assertTemplateUsed(response, "website/home.html")

    def test_placeholder_routes_return_http_200(self):
        for route_name in self.placeholder_routes:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)
