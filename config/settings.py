import importlib.util
import os
from pathlib import Path
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured

try:
    import dj_database_url
except ImportError:  # pragma: no cover - local fallback when deploy deps are unavailable
    dj_database_url = None

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default

    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ImproperlyConfigured(f"{name} must be a valid boolean string.")


def env_int(name, default=0):
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ImproperlyConfigured(f"{name} must be an integer.") from exc


def env_value(name, aliases=None):
    aliases = aliases or []
    for candidate in [name, *aliases]:
        value = os.getenv(candidate)
        if value is not None:
            return value
    return None


def env_list(name, default=None, aliases=None):
    value = env_value(name, aliases=aliases)
    if value is None:
        return list(default or [])
    return [item.strip() for item in value.split(",") if item.strip()]


def dedupe_keep_order(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def build_allowed_hosts(debug, configured_hosts=None, render_hostname=None):
    local_hosts = ["127.0.0.1", "localhost", "[::1]"]
    default_production_hosts = [
        "staging.acoeursconsulting.com",
        "acoeursconsulting.com",
        "www.acoeursconsulting.com",
    ]

    hosts = list(local_hosts)
    if configured_hosts:
        hosts.extend(configured_hosts)
    elif not debug:
        hosts.extend(default_production_hosts)

    if render_hostname:
        hosts.append(render_hostname)

    hosts = dedupe_keep_order(hosts)

    if not debug and "*" in hosts:
        raise ImproperlyConfigured("ALLOWED_HOSTS must not contain '*' when DEBUG is False.")

    return hosts


def validate_origin(origin, debug):
    parsed = urlparse(origin)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ImproperlyConfigured(
            "CSRF_TRUSTED_ORIGINS entries must include a valid http or https scheme."
        )

    hostname = parsed.hostname or ""
    if not debug and hostname not in {"localhost", "127.0.0.1", "::1"} and parsed.scheme != "https":
        raise ImproperlyConfigured(
            "Production CSRF_TRUSTED_ORIGINS entries must use https."
        )

    return origin.rstrip("/")


def build_csrf_trusted_origins(debug, configured_origins=None, render_hostname=None):
    default_production_origins = [
        "https://staging.acoeursconsulting.com",
        "https://acoeursconsulting.com",
        "https://www.acoeursconsulting.com",
    ]

    origins = []
    if configured_origins:
        origins.extend(configured_origins)
    elif not debug:
        origins.extend(default_production_origins)

    if render_hostname:
        origins.append(f"https://{render_hostname}")

    validated = [validate_origin(origin, debug) for origin in origins]
    return dedupe_keep_order(validated)


def normalize_site_url(raw_site_url):
    if raw_site_url is None or not raw_site_url.strip():
        return None

    candidate = raw_site_url.strip().rstrip("/")
    parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ImproperlyConfigured("SITE_URL must be a valid absolute URL.")

    if parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
        return None

    return candidate


DEBUG = env_bool("DEBUG", default=True)

local_secret_key = "dev-only-acoeurs-secret-key-not-for-production"
SECRET_KEY = os.getenv("SECRET_KEY", local_secret_key if DEBUG else "")
if not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY must be set when DEBUG is False.")

render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")
configured_allowed_hosts = env_list(
    "ALLOWED_HOSTS",
    aliases=["DJANGO_ALLOWED_HOSTS"],
)
ALLOWED_HOSTS = build_allowed_hosts(
    debug=DEBUG,
    configured_hosts=configured_allowed_hosts,
    render_hostname=render_hostname,
)

configured_csrf_trusted_origins = env_list(
    "CSRF_TRUSTED_ORIGINS",
    aliases=["DJANGO_CSRF_TRUSTED_ORIGINS"],
)
CSRF_TRUSTED_ORIGINS = build_csrf_trusted_origins(
    debug=DEBUG,
    configured_origins=configured_csrf_trusted_origins,
    render_hostname=render_hostname,
)

SITE_URL = normalize_site_url(env_value("SITE_URL"))
SITE_NOINDEX = env_bool("SITE_NOINDEX", default=False)

WHITENOISE_AVAILABLE = importlib.util.find_spec("whitenoise") is not None
DJ_DATABASE_URL_AVAILABLE = dj_database_url is not None

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
]

if WHITENOISE_AVAILABLE:
    INSTALLED_APPS.insert(
        INSTALLED_APPS.index('django.contrib.staticfiles'),
        'whitenoise.runserver_nostatic',
    )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
]

if WHITENOISE_AVAILABLE:
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

MIDDLEWARE += [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.site_meta',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

sqlite_database = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

database_url = os.getenv("DATABASE_URL")
if database_url:
    if not DJ_DATABASE_URL_AVAILABLE:
        raise ImproperlyConfigured(
            "DATABASE_URL is set but dj-database-url is not installed in this environment."
        )
    DATABASES = {
        'default': dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {'default': sqlite_database}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

if WHITENOISE_AVAILABLE:
    staticfiles_storage_backend = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    staticfiles_storage_backend = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': staticfiles_storage_backend,
    },
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env_bool('SECURE_SSL_REDIRECT', default=not DEBUG)
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = env_int('SECURE_HSTS_SECONDS', default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

if not DEBUG and SECURE_HSTS_SECONDS < 0:
    raise ImproperlyConfigured('SECURE_HSTS_SECONDS must be 0 or greater.')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
