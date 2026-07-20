import re

from django.test import TestCase
from django.test import override_settings
from django.urls import reverse


class WebsiteRouteTests(TestCase):
    placeholder_routes = [
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

    def test_market_entry_service_page_returns_http_200(self):
        response = self.client.get(reverse("business_market_entry"))

        self.assertEqual(response.status_code, 200)

    def test_market_entry_service_page_uses_expected_template(self):
        response = self.client.get(reverse("business_market_entry"))

        self.assertTemplateUsed(response, "website/service_market_entry.html")

    def test_market_entry_service_page_contains_expected_seo_metadata(self):
        response = self.client.get(reverse("business_market_entry"))
        content = response.content.decode()

        self.assertIn(
            "<title>欧洲市场进入与战略｜法国及欧洲市场咨询｜Acoeurs Consulting</title>",
            content,
        )
        self.assertIn(
            'content="Acoeurs Consulting 帮助中国企业评估欧洲市场机会、竞争环境、进入模式、渠道与风险，并制定清晰、可执行的市场进入路径。"',
            content,
        )

    def test_market_entry_service_page_contains_single_h1_breadcrumb_and_required_links(self):
        response = self.client.get(reverse("business_market_entry"))
        content = response.content.decode()

        self.assertContains(response, "在投入资源之前，先建立清晰、可执行的欧洲市场路径")
        self.assertEqual(content.count("<h1"), 1)
        self.assertContains(response, 'aria-label="面包屑"', html=False)
        self.assertContains(response, ">首页</a>", html=False)
        self.assertContains(response, ">企业服务</a>", html=False)
        self.assertContains(response, 'aria-current="page">欧洲市场进入与战略<', html=False)
        self.assertIn(reverse("consultation"), content)
        self.assertIn(reverse("business"), content)
        self.assertIn(reverse("case_listed_company_france"), content)

    def test_market_entry_service_page_contains_scope_headings_and_professional_note(self):
        response = self.client.get(reverse("business_market_entry"))
        content = response.content.decode()

        expected_headings = [
            "市场与赛道评估",
            "竞争与客户研究",
            "进入模式与风险判断",
            "品牌、渠道与商业路径",
            "市场进入路线图",
        ]

        for heading in expected_headings:
            with self.subTest(heading=heading):
                self.assertContains(response, heading)

        self.assertIn("中国上市公司｜法国市场拓展", content)
        self.assertIn(reverse("case_listed_company_france"), content)
        self.assertNotIn("企业进入欧洲前，通常需要先回答这些关键问题", content)
        self.assertNotIn("典型问题", content)
        self.assertNotIn("固定项目周期", content)
        self.assertNotIn("标准套餐", content)
        self.assertNotIn("项目成果", content)
        self.assertNotIn("价格", content)
        self.assertNotIn("4–6 周", content)

    def test_company_banking_service_page_returns_http_200(self):
        response = self.client.get(reverse("business_company_banking"))

        self.assertEqual(response.status_code, 200)

    def test_company_banking_service_page_uses_expected_template(self):
        response = self.client.get(reverse("business_company_banking"))

        self.assertTemplateUsed(response, "website/service_company_banking.html")

    def test_company_banking_service_page_contains_expected_seo_metadata(self):
        response = self.client.get(reverse("business_company_banking"))
        content = response.content.decode()

        self.assertIn(
            "<title>公司架构与银行金融｜法国公司设立与账户准备｜Acoeurs Consulting</title>",
            content,
        )
        self.assertIn(
            'content="Acoeurs Consulting 协助中国企业梳理法国及跨境公司架构，协调公司设立、税务基础登记、银行KYC材料、Fintech账户与支付方案。"',
            content,
        )

    def test_company_banking_service_page_contains_single_h1_breadcrumb_and_required_links(self):
        response = self.client.get(reverse("business_company_banking"))
        content = response.content.decode()

        self.assertContains(response, "让公司结构、经营需求与金融安排从一开始相互匹配")
        self.assertEqual(content.count("<h1"), 1)
        self.assertContains(response, 'aria-label="面包屑"', html=False)
        self.assertContains(response, ">首页</a>", html=False)
        self.assertContains(response, ">企业服务</a>", html=False)
        self.assertContains(response, 'aria-current="page">公司架构与银行金融<', html=False)
        self.assertIn(reverse("consultation"), content)
        self.assertIn(reverse("business"), content)

    def test_company_banking_service_page_contains_scope_headings_and_boundary_copy(self):
        response = self.client.get(reverse("business_company_banking"))
        content = response.content.decode()

        expected_headings = [
            "公司形式与架构梳理",
            "法国公司设立协调",
            "税务与跨境基础登记",
            "银行账户准备与协调",
            "Fintech 与支付配置",
            "公司生命周期事项",
        ]

        for heading in expected_headings:
            with self.subTest(heading=heading):
                self.assertContains(response, heading)

        self.assertIn("银行、支付机构及其他金融机构对账户申请拥有独立审核和决定权。", content)
        self.assertNotIn("保证开户", content)
        self.assertNotIn("开户成功率", content)
        self.assertNotIn("价格", content)
        self.assertNotIn("典型场景", content)
        self.assertNotIn("项目成果", content)
        self.assertNotIn("六个前期问题", content)
        self.assertNotIn("固定项目周期", content)
        self.assertNotIn("4–6 周", content)

    def test_tax_legal_compliance_service_page_returns_http_200(self):
        response = self.client.get(reverse("business_tax_legal_compliance"))

        self.assertEqual(response.status_code, 200)

    def test_tax_legal_compliance_service_page_uses_expected_template(self):
        response = self.client.get(reverse("business_tax_legal_compliance"))

        self.assertTemplateUsed(response, "website/service_tax_legal_compliance.html")

    def test_tax_legal_compliance_service_page_contains_expected_seo_metadata(self):
        response = self.client.get(reverse("business_tax_legal_compliance"))
        content = response.content.decode()

        self.assertIn(
            "<title>财税、法律与合规｜法国企业会计税务与法律协调｜Acoeurs Consulting</title>",
            content,
        )
        self.assertIn(
            'content="Acoeurs Consulting 协调法国企业会计报税、工资社保、跨境申报、GDPR、KYC及法律专业支持，帮助中国企业持续管理本地经营事项。"',
            content,
        )

    def test_tax_legal_compliance_service_page_contains_single_h1_breadcrumb_and_required_links(self):
        response = self.client.get(reverse("business_tax_legal_compliance"))
        content = response.content.decode()

        self.assertContains(response, "让企业在法国的日常经营保持有序、连续并可持续管理")
        self.assertEqual(content.count("<h1"), 1)
        self.assertContains(response, 'aria-label="面包屑"', html=False)
        self.assertContains(response, ">首页</a>", html=False)
        self.assertContains(response, ">企业服务</a>", html=False)
        self.assertContains(response, 'aria-current="page">财税、法律与合规<', html=False)
        self.assertIn(reverse("consultation"), content)
        self.assertIn(reverse("business"), content)

    def test_tax_legal_compliance_service_page_contains_scope_headings_and_boundary_copy(self):
        response = self.client.get(reverse("business_tax_legal_compliance"))
        content = response.content.decode()

        expected_headings = [
            "会计记账与年度申报",
            "工资、社保与人员申报",
            "跨境税务与专项申报",
            "数据、KYC与反洗钱合规",
            "合同与法律事务协调",
        ]

        for heading in expected_headings:
            with self.subTest(heading=heading):
                self.assertContains(response, heading)

        self.assertIn("相关工作由具备相应资质的专业人士提供或执行。", content)
        self.assertNotIn("价格", content)
        self.assertNotIn("固定项目周期", content)
        self.assertNotIn("保证完全合规", content)
        self.assertNotIn("税务最优", content)
        self.assertNotIn("零风险", content)

    def test_local_operations_service_page_returns_http_200(self):
        response = self.client.get(reverse("business_local_operations"))

        self.assertEqual(response.status_code, 200)

    def test_local_operations_service_page_uses_expected_template(self):
        response = self.client.get(reverse("business_local_operations"))

        self.assertTemplateUsed(response, "website/service_local_operations.html")

    def test_local_operations_service_page_contains_expected_seo_metadata(self):
        response = self.client.get(reverse("business_local_operations"))
        content = response.content.decode()

        self.assertIn(
            "<title>本地运营与团队建设｜法国企业运营与团队支持｜Acoeurs Consulting</title>",
            content,
        )
        self.assertIn(
            'content="Acoeurs Consulting 协助中国企业协调法国本地招聘、人员行政、办公与日常运营事项，连接中国总部、本地团队和专业服务方。"',
            content,
        )

    def test_local_operations_service_page_contains_single_h1_breadcrumb_and_required_links(self):
        response = self.client.get(reverse("business_local_operations"))
        content = response.content.decode()

        self.assertContains(response, "让法国本地团队与日常运营真正运转起来")
        self.assertEqual(content.count("<h1"), 1)
        self.assertContains(response, 'aria-label="面包屑"', html=False)
        self.assertContains(response, ">首页</a>", html=False)
        self.assertContains(response, ">企业服务</a>", html=False)
        self.assertContains(response, 'aria-current="page">本地运营与团队建设<', html=False)
        self.assertIn(reverse("consultation"), content)
        self.assertIn(reverse("business"), content)

    def test_local_operations_service_page_contains_scope_headings_and_boundary_copy(self):
        response = self.client.get(reverse("business_local_operations"))
        content = response.content.decode()

        expected_headings = [
            "招聘与团队搭建协调",
            "人员与日常行政协调",
            "办公与运营空间支持",
            "文件、翻译与行政支持",
            "商标与本地运营事项协调",
        ]

        for heading in expected_headings:
            with self.subTest(heading=heading):
                self.assertContains(response, heading)

        self.assertIn("相关工作由具备相应资质的专业人士提供或执行。", content)
        self.assertNotIn("价格", content)
        self.assertNotIn("固定项目周期", content)
        self.assertNotIn("保证招聘成功", content)
        self.assertNotIn("零风险用工", content)
        self.assertNotIn("客户案例", content)

    def test_business_growth_service_page_returns_http_200(self):
        response = self.client.get(reverse("business_growth"))

        self.assertEqual(response.status_code, 200)

    def test_business_growth_service_page_uses_expected_template(self):
        response = self.client.get(reverse("business_growth"))

        self.assertTemplateUsed(response, "website/service_business_growth.html")

    def test_business_growth_service_page_contains_expected_seo_metadata(self):
        response = self.client.get(reverse("business_growth"))
        content = response.content.decode()

        self.assertIn(
            "<title>商务拓展与增长｜法国市场客户渠道与品牌拓展｜Acoeurs Consulting</title>",
            content,
        )
        self.assertIn(
            'content="Acoeurs Consulting 协助中国企业在法国及欧洲推进客户、渠道、合作伙伴、商务活动和本地市场连接事项，并提供持续的法国本地协调支持。"',
            content,
        )

    def test_business_growth_service_page_contains_single_h1_breadcrumb_and_required_links(self):
        response = self.client.get(reverse("business_growth"))
        content = response.content.decode()

        self.assertContains(response, "让企业在法国市场被看见，并建立真实的商业连接")
        self.assertEqual(content.count("<h1"), 1)
        self.assertContains(response, 'aria-label="面包屑"', html=False)
        self.assertContains(response, ">首页</a>", html=False)
        self.assertContains(response, ">企业服务</a>", html=False)
        self.assertContains(response, 'aria-current="page">商务拓展与增长<', html=False)
        self.assertIn(reverse("consultation"), content)
        self.assertIn(reverse("business"), content)

    def test_business_growth_service_page_contains_scope_headings_and_boundary_copy(self):
        response = self.client.get(reverse("business_growth"))
        content = response.content.decode()

        expected_headings = [
            "目标客户与商务接触",
            "渠道与合作伙伴拓展",
            "商务会面与项目推进",
            "展会与行业活动支持",
            "本地资源与长期市场推进",
        ]

        for heading in expected_headings:
            with self.subTest(heading=heading):
                self.assertContains(response, heading)

        self.assertIn("具体合作、签约及业务结果不能预先保证。", content)
        self.assertNotIn("价格", content)
        self.assertNotIn("固定项目周期", content)
        self.assertNotIn("保证获客", content)
        self.assertNotIn("保证签约", content)
        self.assertNotIn("精准获客", content)
        self.assertNotIn("固定客户数量", content)
        self.assertNotIn("客户案例", content)

    def test_personal_services_page_returns_http_200(self):
        response = self.client.get(reverse("personal"))

        self.assertEqual(response.status_code, 200)

    def test_personal_services_page_uses_expected_template(self):
        response = self.client.get(reverse("personal"))

        self.assertTemplateUsed(response, "website/personal_services.html")

    def test_personal_services_page_contains_expected_seo_metadata(self):
        response = self.client.get(reverse("personal"))
        content = response.content.decode()

        self.assertIn(
            "<title>个人服务｜法国居留、家庭与资产事务协调｜Acoeurs Consulting</title>",
            content,
        )
        self.assertIn(
            'content="Acoeurs Consulting 为企业主、投资人与家庭提供法国居留、家庭事务、房产资产及跨境税务等本地协调服务。"',
            content,
        )

    def test_personal_services_page_contains_single_h1_breadcrumb_and_detail_links(self):
        response = self.client.get(reverse("personal"))
        content = response.content.decode()

        self.assertContains(response, "面向企业主、投资人与家庭的法国本地服务")
        self.assertEqual(content.count("<h1"), 1)
        self.assertContains(response, 'aria-label="面包屑"', html=False)
        self.assertContains(response, ">首页</a>", html=False)
        self.assertContains(response, 'aria-current="page">个人服务<', html=False)
        self.assertContains(response, '<a aria-current="page" href="/personal/">个人服务</a>', html=False)
        self.assertNotIn('<a aria-current="page" href="/business/">企业服务</a>', content)
        self.assertIn(reverse("personal_residency_family"), content)
        self.assertIn(reverse("personal_property_wealth"), content)
        self.assertIn(reverse("personal_cross_border_tax_risk"), content)
        self.assertIn(reverse("consultation"), content)

    def test_personal_services_page_contains_service_categories_and_boundary_copy(self):
        response = self.client.get(reverse("personal"))
        content = response.content.decode()

        expected_headings = [
            "居留与家庭定居",
            "房产与资产配置",
            "跨境税务与风险管理",
        ]

        for heading in expected_headings:
            with self.subTest(heading=heading):
                self.assertContains(response, heading)

        self.assertIn("相关决定或专业工作由政府机构、金融机构或具备相应资质的专业人士独立完成。", content)
        self.assertNotIn("价格", content)
        self.assertNotIn("固定办理周期", content)
        self.assertNotIn("保证获批", content)
        self.assertNotIn("保证贷款", content)
        self.assertNotIn("保证升值", content)
        self.assertNotIn("客户案例", content)
        self.assertNotIn("银行级安全", content)

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
