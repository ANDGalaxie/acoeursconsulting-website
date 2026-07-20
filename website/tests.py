import re

from django.test import TestCase
from django.test import override_settings
from django.urls import reverse


class WebsiteRouteTests(TestCase):
    placeholder_routes = [
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

    def test_enterprise_services_page_returns_http_200(self):
        response = self.client.get(reverse("business"))

        self.assertEqual(response.status_code, 200)

    def test_enterprise_services_page_uses_expected_template(self):
        response = self.client.get(reverse("business"))

        self.assertTemplateUsed(response, "website/enterprise_services.html")

    def test_enterprise_services_page_contains_expected_seo_metadata(self):
        response = self.client.get(reverse("business"))
        content = response.content.decode()

        self.assertIn(
            "<title>企业服务｜法国及欧洲市场进入与本地运营｜Acoeurs Consulting</title>",
            content,
        )
        self.assertIn(
            'content="Acoeurs Consulting 为中国企业提供欧洲市场进入、公司架构、财税法律合规、本地运营、团队建设与商务拓展支持。"',
            content,
        )

    def test_enterprise_services_page_contains_single_h1_and_breadcrumb(self):
        response = self.client.get(reverse("business"))
        content = response.content.decode()

        self.assertContains(response, "从市场判断到本地增长，构建可持续的欧洲业务体系")
        self.assertEqual(content.count("<h1"), 1)
        self.assertContains(response, 'aria-label="面包屑"', html=False)
        self.assertContains(response, ">首页</a>", html=False)
        self.assertContains(response, 'aria-current="page">企业服务<', html=False)

    def test_enterprise_services_page_contains_all_service_categories_and_links(self):
        response = self.client.get(reverse("business"))
        content = response.content.decode()

        expected_services = [
            ("欧洲市场进入与战略", "business_market_entry"),
            ("公司架构与银行金融", "business_company_banking"),
            ("财税、法律与合规", "business_tax_legal_compliance"),
            ("本地运营与团队建设", "business_local_operations"),
            ("商务拓展与增长", "business_growth"),
        ]

        for label, route_name in expected_services:
            with self.subTest(label=label):
                self.assertContains(response, label)
                self.assertIn(reverse(route_name), content)

    def test_enterprise_services_page_contains_consultation_links(self):
        response = self.client.get(reverse("business"))
        content = response.content.decode()

        self.assertGreaterEqual(content.count(reverse("consultation")), 2)
        self.assertIn('href="#enterprise-service-scope"', content)

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

    def test_health_endpoint_returns_http_200(self):
        response = self.client.get(reverse("health"))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), {"status": "ok"})

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
    def test_custom_404_template_is_used(self):
        response = self.client.get("/missing-page/")

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertIn("返回首页", response.content.decode())
