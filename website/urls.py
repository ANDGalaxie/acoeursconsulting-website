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
        views.placeholder,
        {"title": "财税、法律与合规", "section": "企业服务"},
        name="business_tax_legal_compliance",
    ),
    path(
        "business/local-operations/",
        views.placeholder,
        {"title": "本地运营与团队建设", "section": "企业服务"},
        name="business_local_operations",
    ),
    path(
        "business/growth/",
        views.placeholder,
        {"title": "商务拓展与增长", "section": "企业服务"},
        name="business_growth",
    ),
    path(
        "personal/",
        views.placeholder,
        {"title": "个人服务", "section": "个人服务总览占位页"},
        name="personal",
    ),
    path(
        "personal/residency-family/",
        views.placeholder,
        {"title": "居留与家庭定居", "section": "个人服务"},
        name="personal_residency_family",
    ),
    path(
        "personal/property-wealth/",
        views.placeholder,
        {"title": "房产与资产配置", "section": "个人服务"},
        name="personal_property_wealth",
    ),
    path(
        "personal/cross-border-tax-risk/",
        views.placeholder,
        {"title": "跨境税务与风险管理", "section": "个人服务"},
        name="personal_cross_border_tax_risk",
    ),
    path(
        "about/",
        views.placeholder,
        {"title": "关于我们", "section": "公司信息"},
        name="about",
    ),
    path(
        "consultation/",
        views.placeholder,
        {"title": "预约咨询", "section": "咨询入口"},
        name="consultation",
    ),
    path(
        "cases/listed-company-france/",
        views.placeholder,
        {"title": "案例：法国上市公司项目", "section": "案例研究"},
        name="case_listed_company_france",
    ),
    path(
        "legal/",
        views.placeholder,
        {"title": "法律声明", "section": "站点信息"},
        name="legal",
    ),
    path(
        "privacy/",
        views.placeholder,
        {"title": "隐私政策", "section": "站点信息"},
        name="privacy",
    ),
    path(
        "cookies/",
        views.placeholder,
        {"title": "Cookies 政策", "section": "站点信息"},
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
