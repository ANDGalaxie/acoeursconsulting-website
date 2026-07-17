import re

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

    def test_homepage_contains_required_sections(self):
        response = self.client.get(reverse("home"))

        required_headings = [
            "扎根法国，连接中国与欧洲",
            "您的欧洲业务正处于哪个阶段？",
            "覆盖欧洲业务全生命周期的企业服务",
            "面向企业主、投资人与家庭的法国本地服务",
            "从判断到执行，一套清晰的项目路径",
            "从市场进入到业务增长的真实实践",
            "为什么选择 Acoeurs",
            "准备开始您的法国及欧洲市场项目？",
        ]

        for heading in required_headings:
            with self.subTest(heading=heading):
                self.assertContains(response, heading)

    def test_homepage_internal_links_resolve(self):
        response = self.client.get(reverse("home"))
        hrefs = set(re.findall(r'href="([^"]+)"', response.content.decode()))

        for href in hrefs:
            if href.startswith("/") and not href.startswith("/static/"):
                with self.subTest(href=href):
                    linked_response = self.client.get(href)
                    self.assertEqual(linked_response.status_code, 200)

    def test_placeholder_routes_return_http_200(self):
        for route_name in self.placeholder_routes:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)

    def test_homepage_footer_contains_confirmed_contact_information(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "contact@acoeursconsulting.com")
        self.assertContains(response, "+33 (0)9 72 96 05 73")
        self.assertContains(response, "400-606-0685")

    def test_homepage_contains_expected_primary_links(self):
        response = self.client.get(reverse("home"))
        content = response.content.decode()

        self.assertIn(reverse("consultation"), content)
        self.assertIn(reverse("case_listed_company_france"), content)
        self.assertIn(reverse("about"), content)

    def test_homepage_footer_contains_expected_navigation_links(self):
        response = self.client.get(reverse("home"))
        content = response.content.decode()

        expected_routes = [
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
            "legal",
            "privacy",
            "cookies",
        ]

        for route_name in expected_routes:
            with self.subTest(route_name=route_name):
                self.assertIn(reverse(route_name), content)
