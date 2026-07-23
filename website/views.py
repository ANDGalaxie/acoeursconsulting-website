import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import ContactForm


logger = logging.getLogger(__name__)


CONTACT_DIRECTION_GROUPS = [
    {
        "key": "company",
        "title": "企业服务方向",
        "identities": ["company"],
        "options": [
            ("business_market_entry", "欧洲市场进入与战略"),
            ("business_company_banking", "公司架构与银行金融"),
            ("business_tax_legal", "财税、法律与合规"),
            ("business_local_operations", "本地运营与团队建设"),
            ("business_growth", "商务拓展与增长"),
            ("other", "其他事项"),
            ("unsure", "暂不确定"),
        ],
    },
    {
        "key": "owner_investor",
        "title": "企业主与投资人常见方向",
        "identities": ["owner_investor"],
        "options": [
            ("business_market_entry", "欧洲市场进入与战略"),
            ("business_company_banking", "公司架构与银行金融"),
            ("business_tax_legal", "财税、法律与合规"),
            ("personal_property_assets", "房产与资产配置"),
            ("personal_cross_border_tax", "跨境税务与风险管理"),
            ("other", "其他事项"),
            ("unsure", "暂不确定"),
        ],
    },
    {
        "key": "individual_family",
        "title": "个人与家庭服务方向",
        "identities": ["individual_family"],
        "options": [
            ("personal_residency_family", "居留与家庭定居"),
            ("personal_property_assets", "房产与资产配置"),
            ("personal_cross_border_tax", "跨境税务与风险管理"),
            ("other", "其他事项"),
            ("unsure", "暂不确定"),
        ],
    },
    {
        "key": "unsure",
        "title": "全部咨询方向",
        "identities": ["unsure"],
        "options": [
            ("business_market_entry", "欧洲市场进入与战略"),
            ("business_company_banking", "公司架构与银行金融"),
            ("business_tax_legal", "财税、法律与合规"),
            ("business_local_operations", "本地运营与团队建设"),
            ("business_growth", "商务拓展与增长"),
            ("personal_residency_family", "居留与家庭定居"),
            ("personal_property_assets", "房产与资产配置"),
            ("personal_cross_border_tax", "跨境税务与风险管理"),
            ("unsure", "暂不确定"),
            ("other", "其他事项"),
        ],
    },
]


def page_context(current_nav=None):
    context = {}
    if current_nav:
        context["current_nav"] = current_nav
    return context


def build_contact_context(form, submitted=False, current_step=1, send_failed=False):
    context = page_context()
    context.update(
        {
            "form": form,
            "submitted": submitted,
            "current_step": current_step,
            "contact_direction_groups": CONTACT_DIRECTION_GROUPS,
            "send_failed": send_failed,
        }
    )
    return context


def get_contact_step_from_errors(form):
    step_fields = {
        1: {"identity", "organization_name"},
        2: {"consultation_direction", "subject", "message"},
        3: {"name", "phone", "email", "preferred_language", "contact_time", "privacy_consent"},
    }
    error_fields = set(form.errors.keys())

    for step, fields in step_fields.items():
        if error_fields.intersection(fields):
            return step

    if error_fields:
        return 3

    return 1


def build_contact_email_subject(form):
    subject = form.cleaned_data.get("subject") or "未填写主题"
    return "【官网咨询】{}｜{}｜{}".format(
        form.get_direction_label(),
        subject,
        form.cleaned_data["name"],
    )


def build_contact_email_body(form):
    timestamp = timezone.localtime().strftime("%Y-%m-%d %H:%M")
    return "\n".join(
        [
            "Acoeurs Consulting 官网收到一条新的联系请求",
            "",
            f"提交时间：{timestamp}",
            f"身份：{form.get_identity_label()}",
            f"公司或机构：{form.cleaned_data.get('organization_name') or '未填写'}",
            f"咨询方向：{form.get_direction_label()}",
            f"咨询主题：{form.cleaned_data.get('subject') or '未填写'}",
            "",
            "咨询内容：",
            form.cleaned_data.get("message") or "未填写",
            "",
            f"姓名：{form.cleaned_data['name']}",
            f"联系电话：{form.cleaned_data.get('phone') or '未填写'}",
            f"电子邮箱：{form.cleaned_data.get('email') or '未填写'}",
            f"沟通语言：{dict(form.fields['preferred_language'].choices).get(form.cleaned_data['preferred_language'])}",
            f"方便联系的时间：{form.cleaned_data.get('contact_time') or '未填写'}",
            "",
            "隐私同意：已同意Acoeurs Consulting为处理本次联系请求而使用所提交的信息",
            "请求来源：Acoeurs Consulting 官网联系表单",
        ]
    )


def send_contact_email(form):
    email = EmailMultiAlternatives(
        subject=build_contact_email_subject(form),
        body=build_contact_email_body(form),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_RECIPIENT_EMAIL],
        reply_to=[form.cleaned_data["email"]] if form.cleaned_data.get("email") else None,
    )
    email.send(fail_silently=False)


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


def contact(request):
    submitted = request.GET.get("submitted") == "1" and request.method == "GET"

    if request.method == "POST":
        form = ContactForm(request.POST)

        if request.POST.get("website", "").strip():
            return redirect(f"{reverse('contact')}?submitted=1", permanent=False)

        if form.is_valid():
            try:
                send_contact_email(form)
            except Exception:
                logger.exception("Contact form email delivery failed.")
                form.add_error(
                    None,
                    "信息暂时未能发送，请稍后重试。您也可以直接发送邮件至 contact@acoeursconsulting.com。",
                )
                return render(
                    request,
                    "website/contact.html",
                    build_contact_context(form=form, current_step=3, send_failed=True),
                )

            return redirect(f"{reverse('contact')}?submitted=1", permanent=False)

        return render(
            request,
            "website/contact.html",
            build_contact_context(form=form, current_step=get_contact_step_from_errors(form)),
        )

    form = ContactForm(initial={"preferred_language": "zh"})
    return render(
        request,
        "website/contact.html",
        build_contact_context(form=form, submitted=submitted, current_step=1),
    )


def consultation_redirect(request):
    return redirect("contact", permanent=True)


def case_study_redirect(request):
    return redirect(f"{reverse('home')}#case-title", permanent=True)


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
