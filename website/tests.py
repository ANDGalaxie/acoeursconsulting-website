import re

import config.settings as project_settings
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse


class WebsiteRouteTests(TestCase):
    placeholder_routes = [
        "consultation",
        "case_listed_company_france",
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

    def test_residency_family_service_page_returns_http_200(self):
        response = self.client.get(reverse("personal_residency_family"))

        self.assertEqual(response.status_code, 200)

    def test_residency_family_service_page_uses_expected_template(self):
        response = self.client.get(reverse("personal_residency_family"))

        self.assertTemplateUsed(response, "website/service_residency_family.html")

    def test_residency_family_service_page_contains_expected_seo_metadata(self):
        response = self.client.get(reverse("personal_residency_family"))
        content = response.content.decode()

        self.assertIn(
            "<title>居留与家庭定居｜法国个人与家庭事务协调｜Acoeurs Consulting</title>",
            content,
        )
        self.assertIn(
            'content="Acoeurs Consulting 协助客户协调法国居留、家庭及相关本地行政事项，并对接相应机构与专业服务方。"',
            content,
        )

    def test_residency_family_service_page_contains_required_content_and_boundaries(self):
        response = self.client.get(reverse("personal_residency_family"))
        content = response.content.decode()

        expected_headings = [
            "居留与身份事项协调",
            "家庭成员与定居事项",
            "子女教育与医疗保障事项",
            "驾照、文件与机构沟通",
        ]

        self.assertContains(response, "协调在法居留与家庭事务，让每一步更容易理解和跟进")
        self.assertEqual(content.count("<h1"), 1)
        self.assertContains(response, 'aria-label="面包屑"', html=False)
        self.assertContains(response, ">首页</a>", html=False)
        self.assertContains(response, ">个人服务</a>", html=False)
        self.assertContains(response, 'aria-current="page">居留与家庭定居<', html=False)
        self.assertContains(response, '<a aria-current="page" href="/personal/">个人服务</a>', html=False)
        self.assertNotIn('<a aria-current="page" href="/business/">企业服务</a>', content)
        self.assertIn(reverse("consultation"), content)
        self.assertIn(reverse("personal"), content)
        self.assertIn("page-service-detail page-personal-service-detail", content)
        self.assertIn("personal-detail-boundary", content)
        self.assertIn("personal-detail-cta", content)
        self.assertIn("personal-detail-cta__secondary-link", content)
        self.assertLess(
            content.index('id="residency-family-note-title"'),
            content.index('id="residency-family-cta-title"'),
        )

        for heading in expected_headings:
            with self.subTest(heading=heading):
                self.assertContains(response, heading)

        self.assertIn("由相关机构独立审查和决定。", content)
        self.assertNotIn("价格", content)
        self.assertNotIn("固定审批周期", content)
        self.assertNotIn("保证获批", content)
        self.assertNotIn("绿色通道", content)
        self.assertNotIn("录取保证", content)
        self.assertNotIn("客户案例", content)

    def test_property_wealth_service_page_returns_http_200(self):
        response = self.client.get(reverse("personal_property_wealth"))

        self.assertEqual(response.status_code, 200)

    def test_property_wealth_service_page_uses_expected_template(self):
        response = self.client.get(reverse("personal_property_wealth"))

        self.assertTemplateUsed(response, "website/service_property_wealth.html")

    def test_property_wealth_service_page_contains_expected_seo_metadata(self):
        response = self.client.get(reverse("personal_property_wealth"))
        content = response.content.decode()

        self.assertIn(
            "<title>房产与资产配置｜法国房产及相关事务协调｜Acoeurs Consulting</title>",
            content,
        )
        self.assertIn(
            'content="Acoeurs Consulting 协助客户协调法国房产购买、持有及相关公证、法律、税务和金融事项。"',
            content,
        )

    def test_property_wealth_service_page_contains_required_content_and_boundaries(self):
        response = self.client.get(reverse("personal_property_wealth"))
        content = response.content.decode()

        expected_headings = [
            "房产购买事项协调",
            "公证、法律与交易文件协调",
            "贷款、持有结构与专业事项协调",
            "持有与后续管理支持",
        ]

        self.assertContains(response, "协调法国房产与相关专业事项，帮助客户掌握每个关键环节")
        self.assertEqual(content.count("<h1"), 1)
        self.assertContains(response, 'aria-label="面包屑"', html=False)
        self.assertContains(response, ">首页</a>", html=False)
        self.assertContains(response, ">个人服务</a>", html=False)
        self.assertContains(response, 'aria-current="page">房产与资产配置<', html=False)
        self.assertContains(response, '<a aria-current="page" href="/personal/">个人服务</a>', html=False)
        self.assertNotIn('<a aria-current="page" href="/business/">企业服务</a>', content)
        self.assertIn(reverse("consultation"), content)
        self.assertIn(reverse("personal"), content)
        self.assertIn("page-service-detail page-personal-service-detail", content)
        self.assertIn("personal-detail-boundary", content)
        self.assertIn("personal-detail-cta", content)
        self.assertIn("personal-detail-cta__secondary-link", content)
        self.assertLess(
            content.index('id="property-assets-note-title"'),
            content.index('id="property-assets-cta-title"'),
        )

        for heading in expected_headings:
            with self.subTest(heading=heading):
                self.assertContains(response, heading)

        self.assertIn("由相应机构或具备资质的专业人士独立审查、决定或执行。", content)
        self.assertNotIn("价格", content)
        self.assertNotIn("固定成交周期", content)
        self.assertNotIn("保证贷款", content)
        self.assertNotIn("保证升值", content)
        self.assertNotIn("投资回报", content)
        self.assertNotIn("客户案例", content)

    def test_cross_border_tax_risk_service_page_returns_http_200(self):
        response = self.client.get(reverse("personal_cross_border_tax_risk"))

        self.assertEqual(response.status_code, 200)

    def test_cross_border_tax_risk_service_page_uses_expected_template(self):
        response = self.client.get(reverse("personal_cross_border_tax_risk"))

        self.assertTemplateUsed(response, "website/service_cross_border_tax_risk.html")

    def test_cross_border_tax_risk_service_page_contains_expected_seo_metadata(self):
        response = self.client.get(reverse("personal_cross_border_tax_risk"))
        content = response.content.decode()

        self.assertIn(
            "<title>跨境税务与风险管理｜中法个人税务事务协调｜Acoeurs Consulting</title>",
            content,
        )
        self.assertIn(
            'content="Acoeurs Consulting 协助客户梳理中法跨境税务、个人申报及家庭资产相关事项，并协调具备资质的专业服务方。"',
            content,
        )

    def test_cross_border_tax_risk_service_page_contains_required_content_and_boundaries(self):
        response = self.client.get(reverse("personal_cross_border_tax_risk"))
        content = response.content.decode()

        expected_headings = [
            "税务居民与协定事项协调",
            "跨境申报与 Exit Tax 事项",
            "家庭资产、继承与赠与事项",
            "保险与风险管理协调",
        ]

        self.assertContains(response, "协调中法跨境税务与家庭资产事项，连接不同专业判断")
        self.assertEqual(content.count("<h1"), 1)
        self.assertContains(response, 'aria-label="面包屑"', html=False)
        self.assertContains(response, ">首页</a>", html=False)
        self.assertContains(response, ">个人服务</a>", html=False)
        self.assertContains(response, 'aria-current="page">跨境税务与风险管理<', html=False)
        self.assertContains(response, '<a aria-current="page" href="/personal/">个人服务</a>', html=False)
        self.assertNotIn('<a aria-current="page" href="/business/">企业服务</a>', content)
        self.assertIn(reverse("consultation"), content)
        self.assertIn(reverse("personal"), content)
        self.assertIn("page-service-detail page-personal-service-detail", content)
        self.assertIn("personal-detail-boundary", content)
        self.assertIn("personal-detail-cta", content)
        self.assertIn("personal-detail-cta__secondary-link", content)
        self.assertLess(
            content.index('id="cross-border-tax-note-title"'),
            content.index('id="cross-border-tax-cta-title"'),
        )

        for heading in expected_headings:
            with self.subTest(heading=heading):
                self.assertContains(response, heading)

        self.assertIn("需要由相关机构或具备相应资质的专业人士根据客户实际情况判断和执行。", content)
        self.assertNotIn("价格", content)
        self.assertNotIn("固定周期", content)
        self.assertNotIn("税务最优", content)
        self.assertNotIn("合法避税", content)
        self.assertNotIn("固定节税结果", content)
        self.assertNotIn("零风险", content)
        self.assertNotIn("投资收益保证", content)

    def test_about_page_returns_http_200(self):
        response = self.client.get(reverse("about"))

        self.assertEqual(response.status_code, 200)

    def test_about_page_uses_expected_template(self):
        response = self.client.get(reverse("about"))

        self.assertTemplateUsed(response, "website/about.html")

    def test_about_page_contains_expected_seo_metadata(self):
        response = self.client.get(reverse("about"))
        content = response.content.decode()

        self.assertIn(
            "<title>关于Acoeurs｜法国及欧洲市场咨询与本地执行｜Acoeurs Consulting</title>",
            content,
        )
        self.assertIn(
            'content="Acoeurs Consulting 专注中国企业在法国和欧洲市场的进入、落地与持续运营，并为企业主、投资人与家庭提供法国本地事务协调服务。"',
            content,
        )

    def test_about_page_contains_required_content_links_and_navigation_state(self):
        response = self.client.get(reverse("about"))
        content = response.content.decode()

        self.assertEqual(content.count("<h1"), 1)
        self.assertContains(response, "扎根法国，连接中国与欧洲")
        self.assertContains(response, 'aria-label="面包屑"', html=False)
        self.assertContains(response, ">首页</a>", html=False)
        self.assertContains(response, 'aria-current="page">关于我们<', html=False)
        self.assertContains(response, '<a aria-current="page" href="/about/">关于我们</a>', html=False)
        self.assertNotIn('<a aria-current="page" href="/business/">企业服务</a>', content)
        self.assertNotIn('<a aria-current="page" href="/personal/">个人服务</a>', content)
        self.assertIn(reverse("consultation"), content)
        self.assertIn(reverse("business"), content)
        self.assertIn(reverse("personal"), content)
        self.assertContains(response, "企业服务")
        self.assertContains(response, "个人服务")

    def test_about_page_contains_confirmed_roles_and_reasons_without_unverified_claims(self):
        response = self.client.get(reverse("about"))
        content = response.content.decode()

        required_roles = [
            "法国本地执行",
            "中法双语协同",
            "统一项目管理",
            "长期陪伴",
        ]
        required_reasons = [
            "法国本地执行",
            "中法沟通能力",
            "统一事项窗口",
            "长期项目支持",
        ]

        for item in required_roles:
            with self.subTest(role=item):
                self.assertContains(response, item)

        for item in required_reasons:
            with self.subTest(reason=item):
                self.assertContains(response, item)

        self.assertNotIn("500", content)
        self.assertNotIn("92%", content)
        self.assertNotIn("15+", content)
        self.assertNotIn("10+", content)
        self.assertNotIn("团队人数", content)
        self.assertNotIn("创始人", content)
        self.assertNotIn("客户Logo", content)
        self.assertNotIn("价格", content)

    def test_cookie_policy_page_returns_http_200(self):
        response = self.client.get(reverse("cookies"))

        self.assertEqual(response.status_code, 200)

    def test_cookie_policy_page_uses_expected_template(self):
        response = self.client.get(reverse("cookies"))

        self.assertTemplateUsed(response, "website/cookie_policy.html")

    def test_cookie_policy_page_contains_current_cookie_facts(self):
        response = self.client.get(reverse("cookies"))
        content = response.content.decode()

        self.assertEqual(content.count("<h1"), 1)
        self.assertIn("<title>Cookie政策｜Acoeurs Consulting</title>", content)
        self.assertContains(response, "csrftoken")
        self.assertContains(response, "sessionid")
        self.assertContains(response, "未发现访问分析 Cookie、广告 Cookie")
        self.assertContains(response, "当前未设置 Cookie 同意 Banner")
        self.assertNotIn("继续浏览即表示同意", content)
        self.assertIn(reverse("legal"), content)
        self.assertIn(reverse("privacy"), content)

    def test_privacy_policy_page_returns_http_200(self):
        response = self.client.get(reverse("privacy"))

        self.assertEqual(response.status_code, 200)

    def test_privacy_policy_page_uses_expected_template(self):
        response = self.client.get(reverse("privacy"))

        self.assertTemplateUsed(response, "website/privacy_policy.html")

    def test_privacy_policy_page_contains_current_processing_and_boundaries(self):
        response = self.client.get(reverse("privacy"))
        content = response.content.decode()

        self.assertEqual(content.count("<h1"), 1)
        self.assertIn("<title>隐私政策｜Acoeurs Consulting</title>", content)
        self.assertContains(response, "服务器访问和安全日志")
        self.assertContains(response, "用户主动发送的电子邮件")
        self.assertContains(response, "Render 提供应用和数据库托管")
        self.assertContains(response, "访问、更正、删除、限制处理、反对处理和数据可携带")
        self.assertContains(response, "向法国国家信息与自由委员会（CNIL）提出投诉")
        self.assertContains(response, "网站当前未启用在线咨询表单")
        self.assertNotIn("保存 30 天", content)
        self.assertNotIn("银行级加密", content)
        self.assertNotIn("绝对保密", content)
        self.assertNotIn("HiChina 提供网站托管", content)
        self.assertNotIn("zhe jiang", content)
        self.assertNotIn("数据控制者地址位于中国", content)

    def test_legal_notice_page_returns_http_200(self):
        response = self.client.get(reverse("legal"))

        self.assertEqual(response.status_code, 200)

    def test_legal_notice_page_uses_expected_template(self):
        response = self.client.get(reverse("legal"))

        self.assertTemplateUsed(response, "website/legal_notice.html")

    def test_legal_notice_page_stays_in_development_stage_and_avoids_unverified_fields(self):
        response = self.client.get(reverse("legal"))
        content = response.content.decode()

        self.assertEqual(content.count("<h1"), 1)
        self.assertIn("<title>法律声明｜Acoeurs Consulting</title>", content)
        self.assertContains(response, "完整法律声明将在运营主体和托管信息确认后、网站正式上线前发布")
        self.assertContains(response, "acoeursconsulting.com")
        self.assertContains(response, "contact@acoeursconsulting.com")
        self.assertContains(response, "400-606-0685")
        self.assertContains(response, "+33 (0)9 72 96 05 73")
        self.assertContains(response, "Render 提供应用和数据库技术托管")
        self.assertNotIn("SIREN：", content)
        self.assertNotIn("注册资本", content)
        self.assertNotIn("TVA", content)
        self.assertNotIn("成立于 2022", content)
        self.assertNotIn("HiChina 提供网站托管", content)
        self.assertNotIn("2732990287_DOMAIN_COM-VRSN", content)
        self.assertNotIn("DomainAbuse@service.aliyun.com", content)
        self.assertNotIn("2026-10-19", content)
        self.assertNotIn("zhe jiang", content)
        self.assertNotIn("最终正式版本", content)

    def test_internal_legal_documents_include_domain_management_reminders(self):
        with open("docs/LEGAL_NOTICE_DRAFT.md", encoding="utf-8") as draft_file:
            draft = draft_file.read()
        with open("docs/legal-info-checklist.md", encoding="utf-8") as checklist_file:
            checklist = checklist_file.read()

        self.assertIn("Alibaba Cloud Computing Ltd. d/b/a HiChina", draft)
        self.assertIn("2026-10-19", checklist)
        self.assertIn("自动续费是否开启", checklist)
        self.assertIn("DNSSEC", checklist)

    def test_public_legal_notice_does_not_expose_internal_domain_management_details(self):
        response = self.client.get(reverse("legal"))
        content = response.content.decode()

        self.assertNotIn("Registrar IANA ID", content)
        self.assertNotIn("DNS7.HICHINA.COM", content)
        self.assertNotIn("DNS8.HICHINA.COM", content)
        self.assertNotIn("unsigned", content)
        self.assertNotIn("自动续费", content)

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

    def test_allowed_hosts_builder_keeps_localhost_and_staging(self):
        hosts = project_settings.build_allowed_hosts(
            debug=False,
            configured_hosts=["staging.acoeursconsulting.com"],
            render_hostname=None,
        )

        self.assertIn("localhost", hosts)
        self.assertIn("127.0.0.1", hosts)
        self.assertIn("[::1]", hosts)
        self.assertIn("staging.acoeursconsulting.com", hosts)

    def test_allowed_hosts_builder_appends_render_hostname(self):
        hosts = project_settings.build_allowed_hosts(
            debug=False,
            configured_hosts=["staging.acoeursconsulting.com"],
            render_hostname="acoeursconsulting-web.onrender.com",
        )

        self.assertIn("acoeursconsulting-web.onrender.com", hosts)

    def test_allowed_hosts_builder_rejects_wildcard_in_production(self):
        with self.assertRaises(ImproperlyConfigured):
            project_settings.build_allowed_hosts(
                debug=False,
                configured_hosts=["*"],
                render_hostname=None,
            )

    def test_csrf_trusted_origins_builder_requires_https_for_staging(self):
        origins = project_settings.build_csrf_trusted_origins(
            debug=False,
            configured_origins=["https://staging.acoeursconsulting.com"],
            render_hostname=None,
        )

        self.assertIn("https://staging.acoeursconsulting.com", origins)

    def test_csrf_trusted_origins_builder_rejects_entries_without_scheme(self):
        with self.assertRaises(ImproperlyConfigured):
            project_settings.build_csrf_trusted_origins(
                debug=False,
                configured_origins=["staging.acoeursconsulting.com"],
                render_hostname=None,
            )

    @override_settings(SITE_URL="http://localhost:8000", SITE_NOINDEX=False)
    def test_site_url_does_not_emit_localhost_canonical(self):
        response = self.client.get(reverse("home"))
        content = response.content.decode()

        self.assertNotIn('<link rel="canonical"', content)
        self.assertNotIn("localhost:8000", content)

    @override_settings(
        SITE_URL="https://staging.acoeursconsulting.com",
        SITE_NOINDEX=True,
    )
    def test_staging_can_output_noindex_and_staging_canonical(self):
        response = self.client.get(reverse("business"))
        content = response.content.decode()

        self.assertIn('content="noindex, nofollow"', content)
        self.assertIn(
            '<link rel="canonical" href="https://staging.acoeursconsulting.com/business/">',
            content,
        )

    @override_settings(
        SITE_URL="https://acoeursconsulting.com",
        SITE_NOINDEX=False,
    )
    def test_production_can_disable_noindex(self):
        response = self.client.get(reverse("about"))
        content = response.content.decode()

        self.assertNotIn('content="noindex, nofollow"', content)
        self.assertIn(
            '<link rel="canonical" href="https://acoeursconsulting.com/about/">',
            content,
        )

    def test_settings_do_not_include_real_secret_key(self):
        self.assertNotEqual(settings.SECRET_KEY, "")
        self.assertNotIn("sk_live", settings.SECRET_KEY.lower())

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
    def test_custom_404_template_is_used(self):
        response = self.client.get("/missing-page/")

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertIn("返回首页", response.content.decode())
