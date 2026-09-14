from urllib.parse import urljoin, urlsplit

from django.conf import settings
from django.urls import translate_url
from django.utils.translation import get_language

from .seo import PUBLIC_PAGE_ROUTES


def site_meta(request):
    site_url = settings.SITE_URL
    if site_url and urlsplit(site_url).hostname in {'localhost', '127.0.0.1', '::1'}:
        site_url = None
    match = request.resolver_match
    public_page = match is not None and match.url_name in PUBLIC_PAGE_ROUTES
    canonical_url = None
    if site_url and public_page:
        canonical_url = urljoin(f"{site_url.rstrip('/')}/", request.path.lstrip("/"))

    language = getattr(request, 'LANGUAGE_CODE', get_language()) or 'zh'
    html_tags = {'zh': 'zh-Hans', 'fr': 'fr', 'en': 'en'}
    switch_urls = []
    alternates = []
    for code, label in settings.LANGUAGES:
        # translate_url resolves the logical route and preserves query parameters.
        path = translate_url(request.get_full_path(), code)
        switch_urls.append({
            'code': code, 'label': '中文' if code == 'zh' else label,
            'short_label': {'zh': '中文', 'fr': 'FR', 'en': 'EN'}[code],
            'html_lang': html_tags[code], 'url': path,
        })
        if public_page:
            seo_path = translate_url(request.path, code)
            url = urljoin(f"{site_url.rstrip('/')}/", seo_path.lstrip('/')) if site_url else seo_path
            alternates.append({'hreflang': html_tags[code], 'url': url})
    if alternates:
        alternates.append({'hreflang': 'x-default', 'url': alternates[0]['url']})

    return {
        'current_language': language,
        'html_language': html_tags.get(language, 'zh-Hans'),
        'language_switch_urls': switch_urls,
        'language_alternate_urls': alternates,
        "site_canonical_url": canonical_url,
        "site_noindex": settings.SITE_NOINDEX or not public_page or (
            match.url_name == "contact" and bool(request.GET)
        ),
    }
