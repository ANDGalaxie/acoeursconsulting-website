# Multilingual implementation report

Date: 2026-09-14

MULTILINGUAL_STATUS = COMPLETE_WITH_REVIEW_ITEMS

## URL architecture

The existing local working tree was the source of truth; it was clean before this task. One set of Django templates, CSS and vanilla JavaScript serves all 13 formal pages in Chinese, French and English (39 URLs).

- `/` returns HTTP 302 to `/zh/`, regardless of Accept-Language or a pre-existing language cookie.
- `i18n_patterns` prefixes public pages and existing redirects with `/zh/`, `/fr/`, `/en/`. Business slugs and URL names are unchanged.
- Personal detail redirects stay redirects. Consultation and case redirects preserve the selected language, including the case anchor.
- `/admin/`, `/health/`, `/robots.txt` and `/sitemap.xml` remain unprefixed.
- Old `fr` / `en` placeholder routes, the unused placeholder view and its template were removed.

## Django settings and LocaleMiddleware

`LANGUAGE_CODE = "zh"`; `LANGUAGES = [("zh", "简体中文"), ("fr", "Français"), ("en", "English")]`; `USE_I18N = True`; `LOCALE_PATHS = [BASE_DIR / "locale"]`.

LocaleMiddleware is between SessionMiddleware and CommonMiddleware. Public page language comes from the URL. No `set_language` endpoint or language preference cookie was introduced.

Django 5.2 does not ship a default `zh` catalog and otherwise fails during startup with this required default code. The minimal `locale/zh/LC_MESSAGES/django.po` and `.mo` establish that alias and translate only four framework validation messages. Chinese website text is not duplicated into a Chinese catalog. Keep this minimal compiled catalog available during clean checkouts; if all `.mo` files are deliberately removed, first run `msgfmt locale/zh/LC_MESSAGES/django.po -o locale/zh/LC_MESSAGES/django.mo` before Django management commands.

## Templates and Python strings converted

All 13 formal page templates, base, header, footer and existing 400/403/404/500 templates use native `translate` / `blocktranslate`. Meta titles/descriptions, existing Open Graph fields, breadcrumbs, buttons, alt text and accessible labels are included. Header navigation uses gettext context `navigation` for concise labels.

`website/forms.py`: labels, choices, required/invalid messages and validation errors use `gettext_lazy`. Values and validation constraints are unchanged.

`website/views.py`: consultation groups and visible send-failure messages are lazy translations. GET defaults the communication language to the current URL language. Successful and honeypot POST redirects retain it. Internal email formatting, recipient, sender and Reply-To are retained; an `override("zh")` around email construction keeps translated choice labels in the established Chinese working format. No automatic customer reply was added.

The navigation and contact scripts read translated strings from DOM text/data attributes. No empty `djangojs.po`, JavaScript catalog endpoint or additional runtime dependency was added. Browser required and email validation messages follow the page language.

## Translation catalogs

- `locale/fr/LC_MESSAGES/django.po` and `.mo`: 917 translated messages.
- `locale/en/LC_MESSAGES/django.po` and `.mo`: 917 translated messages.
- `locale/zh/LC_MESSAGES/django.po` and `.mo`: minimal framework alias, not a duplicate website translation.
- UTF-8, accented French characters and typographic apostrophes retained.
- Standard Django extraction and compilation completed using GNU gettext 0.21. The environment initially lacked msgfmt/xgettext. The Ubuntu gettext package was downloaded and extracted into a temporary project directory; no system installation or application dependency was required. Temporary tools were removed after verification.
- No blank or fuzzy public translations. Compiled catalogs were exercised through real HTTP responses and browser sessions.

## Language switch behavior

Desktop: 中文 / FR / EN. Mobile/tablet menu: 中文 / Français / English. Active links use `aria-current="page"`, with `lang` and `hreflang` attributes. The existing brand mark and wordmark are unchanged.

`translate_url` resolves the same logical page in the target language and retains query parameters. Switching uses ordinary GET links. A language preference cookie is neither set nor required. Browser checks confirmed same-page switching and absence of `django_language`. Existing necessary CSRF behavior remains.

HTML language tags: zh → zh-Hans, fr → fr, en → en.

## SEO

Canonical and existing og:url point to the current language page without query parameters. Alternates provide zh-Hans, fr, en and x-default for the same logical page; x-default points to its Chinese URL. A configured SITE_URL supplies the absolute origin. Without it, canonical is omitted and alternates use relative paths. Localhost origins are excluded from metadata.

The existing sitemap exposes all 39 formal page URLs when indexing and SITE_URL are enabled. Existing noindex controls remain; robots no longer treats French/English as placeholder directories to disallow. No hosting, DNS or production environment configuration was changed.

## Chinese content and legal status

Rendered main-content text was compared against pre-edit local snapshots for every formal page. All Chinese text was unchanged except the explicitly requested update to the obsolete Cookie-page LocaleMiddleware statement: language now follows the URL prefix, with no dependency on a language preference cookie.

The original test suite contained two expectations for legal wording absent from the current local templates (a 12-month retention proposal and a pre-launch legal publication notice). Their assertions now verify the existing local Chinese source instead of restoring obsolete text. Other substantive Chinese regressions remain covered.

ZH_LEGAL_TEXT = SOURCE_DRAFT
FR_LEGAL_TEXT = TRANSLATION_DRAFT_REQUIRES_COUNSEL
EN_LEGAL_TEXT = TRANSLATION_DRAFT_REQUIRES_COUNSEL

These statuses are internal only. No company identifiers, registered-office assertion, service promise, hosting/provider designation or legal conclusion was added. Statistics were preserved without attestation. The public email remains info@acoeursconsulting.com.

## Visual QA

Real headless local Google Chrome, using the existing Playwright runtime, inspected all 39 URLs at 1920×1080, 1440×900, 1366×768, 390×844, 430×932 and 768×1024 (234 page/viewport combinations). No document horizontal overflow, out-of-viewport public text, missing mobile language menu or JavaScript exception was detected. Legal tables retain their existing local scrolling behavior.

Manual screenshot review covered French/English home heroes, French service hero, French mobile homepage/menu, contact form, privacy contents and footer. Latin-script content uses existing local Latin font fallbacks; the brand wordmark retains its original styling. Limited heading wrapping/font sizing and switcher spacing changes preserve imagery, theme, section order and hero height rules. The hamburger breakpoint is 1024px so tablet navigation has room for all languages. The skip link now hides by its own height to accommodate longer translations and remains visible on keyboard focus.

Nine full contact flows (three languages at desktop and both mobile widths) exercised identity selection, direction selection, optional details, next-step progression, preferred language and submission. Browser POSTs were intercepted locally; Django mail tests use the in-memory backend. No external SMTP was used.

Final focused checks cover the changed service hero, contact and legal pages in all three languages and all six sizes. Machine-readable results are stored in `qa/`; selected review screenshots are stored there as well. Chromium checks do not constitute Safari/Firefox or physical-device certification.

## Tests and commands

- `git status --short` before editing: clean.
- Repository inspection, including local AGENTS.md and all relevant templates, forms, scripts and SEO code.
- `apt-get download gettext` and `dpkg-deb -x ...` in a temporary directory; GNU gettext 0.21 verified.
- `./.venv/bin/python manage.py makemessages -l fr -l en --no-obsolete --ignore=.venv --ignore=.i18n-tools --ignore=.i18n-*.py`: passed with the extracted gettext binary/lib directories on PATH/LD_LIBRARY_PATH.
- `./.venv/bin/python manage.py compilemessages --ignore=.venv --ignore=.i18n-tools`: passed.
- `./.venv/bin/python manage.py check`: passed, no issues.
- `./.venv/bin/python manage.py test website`: 127 tests passed.
- `./.venv/bin/python manage.py makemigrations --check --dry-run`: no changes.
- `git diff --check`: passed.
- Existing rg executable used for the final obsolete-email scan; no match in config, website, templates or static.
- Local browser QA scripts and temporary `manage.py runserver ... --noreload` only. The temporary server was stopped after review.

Native maintenance commands with GNU gettext installed:

```bash
./.venv/bin/python manage.py makemessages -l fr -l en --no-obsolete
./.venv/bin/python manage.py compilemessages
./.venv/bin/python manage.py check
./.venv/bin/python manage.py test website
```

Native architecture reference: [Django 5.2 internationalization](https://docs.djangoproject.com/en/5.2/topics/i18n/translation/).

## Files created

- locale/{zh,fr,en}/LC_MESSAGES/django.po and django.mo
- website/test_i18n.py
- docs/i18n/TRANSLATION_GLOSSARY.md
- docs/i18n/MULTILINGUAL_IMPLEMENTATION_REPORT.md
- docs/i18n/qa/ results and selected browser screenshots

## Files modified

- config/settings.py
- config/urls.py
- static/css/base.css
- static/css/components.css
- static/js/contact.js
- static/js/main.js
- templates/400.html
- templates/403.html
- templates/404.html
- templates/500.html
- templates/base.html
- templates/includes/footer.html
- templates/includes/header.html
- templates/website/about.html
- templates/website/contact.html
- templates/website/cookie_policy.html
- templates/website/enterprise_services.html
- templates/website/home.html
- templates/website/legal_notice.html
- templates/website/personal_services.html
- templates/website/privacy_policy.html
- templates/website/service_business_growth.html
- templates/website/service_company_banking.html
- templates/website/service_local_operations.html
- templates/website/service_market_entry.html
- templates/website/service_tax_legal_compliance.html
- website/context_processors.py
- website/forms.py
- website/tests.py
- website/urls.py
- website/views.py

## Files removed

- templates/website/placeholder.html (no remaining references)

## Known review items and next step

- Qualified counsel must review the French and English legal drafts against the Chinese source draft, and confirm legal/company facts before publication.
- Leadership must confirm the existing statistical claims and company/service facts in the separate readiness review.
- Native-speaker editorial sign-off is recommended for the new business copy; no translation placeholders or known untranslated public UI remain.
- Browser coverage is Chrome with desktop/tablet/mobile viewports; physical devices and other browser engines were not exercised.

No commit, push, deployment, DNS/Render change, production database/SMTP access, secret, analytics, cookie banner, language cookie or new site image was introduced.

NEXT_STEP = PRE-DEPLOYMENT READINESS
