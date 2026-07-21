from urllib.parse import urljoin, urlparse

from django.conf import settings


def site_meta(request):
    canonical_url = None
    site_url = settings.SITE_URL
    if site_url:
        parsed = urlparse(site_url)
        if parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
            canonical_url = urljoin(f"{site_url.rstrip('/')}/", request.path.lstrip("/"))

    return {
        "site_canonical_url": canonical_url,
        "site_noindex": settings.SITE_NOINDEX,
    }
