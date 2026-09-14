from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags


IDENTITY_CHOICES = [
    ("company", _("企业或机构")),
    ("owner_investor", _("企业主或投资人")),
    ("individual_family", _("个人或家庭")),
    ("unsure", _("暂不确定")),
]

DIRECTION_CHOICES = [
    ("business_market_entry", _("欧洲市场进入与战略")),
    ("business_company_banking", _("公司架构与银行金融")),
    ("business_tax_legal", _("财税、法律与合规")),
    ("business_local_operations", _("本地运营与团队建设")),
    ("business_growth", _("商务拓展与增长")),
    ("personal_residency_family", _("居留与家庭定居")),
    ("personal_property_assets", _("房产与资产配置")),
    ("personal_cross_border_tax", _("跨境税务与风险管理")),
    ("unsure", _("暂不确定")),
    ("other", _("其他事项")),
]

DIRECTION_LABELS = dict(DIRECTION_CHOICES)
IDENTITY_LABELS = dict(IDENTITY_CHOICES)

ALLOWED_DIRECTIONS_BY_IDENTITY = {
    "company": {
        "business_market_entry",
        "business_company_banking",
        "business_tax_legal",
        "business_local_operations",
        "business_growth",
        "unsure",
        "other",
    },
    "owner_investor": {
        "business_market_entry",
        "business_company_banking",
        "business_tax_legal",
        "personal_property_assets",
        "personal_cross_border_tax",
        "unsure",
        "other",
    },
    "individual_family": {
        "personal_residency_family",
        "personal_property_assets",
        "personal_cross_border_tax",
        "unsure",
        "other",
    },
    "unsure": {
        "business_market_entry",
        "business_company_banking",
        "business_tax_legal",
        "business_local_operations",
        "business_growth",
        "personal_residency_family",
        "personal_property_assets",
        "personal_cross_border_tax",
        "unsure",
        "other",
    },
}


class ContactForm(forms.Form):
    identity = forms.ChoiceField(
        label=_("您以什么身份联系我们？"),
        choices=IDENTITY_CHOICES,
        widget=forms.RadioSelect,
        error_messages={"required": _("请选择最接近您当前情况的一项。")},
    )
    organization_name = forms.CharField(
        label=_("公司或机构名称"),
        max_length=200,
        required=False,
    )
    consultation_direction = forms.ChoiceField(
        label=_("咨询方向"),
        choices=DIRECTION_CHOICES,
        widget=forms.RadioSelect,
        error_messages={"required": _("请选择最接近的咨询方向。")},
    )
    subject = forms.CharField(
        label=_("咨询主题（选填）"),
        max_length=150,
        required=False,
    )
    message = forms.CharField(
        label=_("情况描述（选填）"),
        max_length=3000,
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        error_messages={
            "max_length": _("咨询内容不能超过 3000 个字符。"),
        },
    )
    name = forms.CharField(
        label=_("姓名"),
        max_length=100,
        error_messages={"required": _("请填写您的姓名。")},
    )
    phone = forms.CharField(
        label=_("联系电话"),
        max_length=50,
        required=False,
    )
    email = forms.EmailField(
        label=_("电子邮箱"),
        max_length=254,
        required=False,
        error_messages={"invalid": _("请输入有效的电子邮箱地址。")},
    )
    preferred_language = forms.ChoiceField(
        label=_("希望使用的沟通语言"),
        choices=[
            ("zh", _("中文")),
            ("fr", "Français"),
            ("en", "English"),
        ],
        initial="zh",
    )
    contact_time = forms.CharField(
        label=_("方便联系的时间"),
        max_length=150,
        required=False,
    )
    privacy_consent = forms.BooleanField(
        label=_("我已阅读并同意《隐私政策》，并同意Acoeurs Consulting为处理本次联系请求而使用我提交的信息。"),
        error_messages={"required": _("请先阅读并同意隐私政策。")},
    )
    website = forms.CharField(required=False, max_length=200)

    def clean_subject(self):
        return strip_tags(self.cleaned_data.get("subject", "")).strip()

    def clean_message(self):
        return strip_tags(self.cleaned_data.get("message", "")).strip()

    def clean_name(self):
        value = strip_tags(self.cleaned_data["name"]).strip()
        if not value:
            raise forms.ValidationError(_("请填写您的姓名。"))
        return value

    def clean_organization_name(self):
        return strip_tags(self.cleaned_data.get("organization_name", "")).strip()

    def clean_phone(self):
        return strip_tags(self.cleaned_data.get("phone", "")).strip()

    def clean_contact_time(self):
        return strip_tags(self.cleaned_data.get("contact_time", "")).strip()

    def clean_website(self):
        return self.cleaned_data.get("website", "").strip()

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone", "").strip()
        email = cleaned_data.get("email", "").strip()
        identity = cleaned_data.get("identity")
        direction = cleaned_data.get("consultation_direction")

        if not phone and not email:
            message = _("请至少填写联系电话或电子邮箱中的一项。")
            self.add_error("phone", message)
            self.add_error("email", message)

        if identity and direction:
            allowed_directions = ALLOWED_DIRECTIONS_BY_IDENTITY.get(identity, set())
            if direction not in allowed_directions:
                self.add_error("consultation_direction", _("请根据您的身份选择合适的咨询方向。"))

        return cleaned_data

    def get_identity_label(self):
        return IDENTITY_LABELS.get(self.cleaned_data.get("identity"), _("未填写"))

    def get_direction_label(self):
        return DIRECTION_LABELS.get(self.cleaned_data.get("consultation_direction"), _("未填写"))
