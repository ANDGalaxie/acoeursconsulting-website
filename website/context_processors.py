from urllib.parse import urljoin

from django.conf import settings

from .seo import PUBLIC_PAGE_ROUTES


def site_meta(request):
    match = request.resolver_match
    public_page = match is not None and match.url_name in PUBLIC_PAGE_ROUTES
    canonical_url = None
    if settings.SITE_URL and public_page:
        canonical_url = urljoin(f"{settings.SITE_URL.rstrip('/')}/", request.path.lstrip("/"))

    return {
        "site_canonical_url": canonical_url,
        "site_noindex": settings.SITE_NOINDEX or not public_page or (
            match.url_name == "contact" and bool(request.GET)
        ),
    }
