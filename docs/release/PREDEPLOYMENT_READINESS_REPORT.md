# Acoeurs Consulting Pre-deployment Readiness Report

Audit date: 2026-09-15

Repository: `ANDGalaxie/acoeursconsulting-website`

Overall status: `READY_WITH_KNOWN_POST_DEPLOYMENT_ITEMS`

This report assesses whether the current codebase can enter its first production deployment while remaining unavailable to the public. It does not approve public launch and does not provide legal advice.

## 1. Executive Summary

| Area | Status | Finding |
|---|---|---|
| Production deployment | READY | No technical deployment blocker was found. |
| First deployment indexing | READY | Deploy with `SITE_NOINDEX=True`; production mode defaults to noindex when the variable is omitted. |
| Public launch | BLOCKED | Legal facts, counsel review, claim substantiation and unresolved image rights remain open. |
| Platform facts | NEEDS_DEPLOYMENT_FACT | Hosting, database, SMTP, DNS, logs, actual cookies and network requests must be recorded after deployment. |
| Access gate | NEEDS_DEPLOYMENT_FACT | Add Basic Auth, an IP allowlist or a maintenance gate during deployment if the platform supports it. |

## 2. Public Page Inventory

The canonical inventory is defined by `website.seo.PUBLIC_PAGE_ROUTES`. All 13 logical pages return HTTP 200 in Chinese, French and English, for a total of 39 canonical language URLs.

| Logical page | URL suffix | Status |
|---|---|---|
| Homepage | `/` | READY |
| Business Services | `/business/` | READY |
| Market Entry | `/business/market-entry/` | READY |
| Company & Banking | `/business/company-banking/` | READY |
| Tax / Legal / Compliance | `/business/tax-legal-compliance/` | READY |
| Local Operations | `/business/local-operations/` | READY |
| Business Growth | `/business/growth/` | READY |
| Personal Services | `/personal/` | READY |
| About | `/about/` | READY |
| Contact | `/contact/` | READY |
| Legal Notice | `/legal/` | READY |
| Privacy Policy | `/privacy/` | READY |
| Cookie Policy | `/cookies/` | READY |

Each suffix is published under `/zh/`, `/fr/` and `/en/`.

Redirect-only routes are not canonical and are excluded from the sitemap:

- `personal/residency-family/` → `personal/`
- `personal/property-wealth/` → `personal/`
- `personal/cross-border-tax-risk/` → `personal/`
- `consultation/` → `contact/`
- `cases/listed-company-france/` → homepage `#case-title`

The redirect target keeps the current language. Infrastructure URLs are `/admin/`, `/health/`, `/robots.txt` and `/sitemap.xml`. Error responses use `400.html`, `403.html`, `404.html` and `500.html`; they are not canonical pages.

## 3. Company Facts

| Public fact | Status | Audit result |
|---|---|---|
| Acoeurs Consulting / 艾克斯咨询 | READY | Brand naming is consistent where shown. |
| `info@acoeursconsulting.com` | READY | Footer, Contact, Legal, Privacy, Cookie and mail defaults use this address. |
| `400-606-0685` | READY | Footer, Contact and Legal use the same display and telephone link. |
| `+33 (0)9 72 96 05 73` | READY | Footer, Contact and Legal use the same display and telephone link. |
| `32 AV. Kléber, 75116 Paris, France` | READY | Legal Notice labels it as a Paris contact address, not a registered office. |
| `acoeursconsulting.com` / `www.acoeursconsulting.com` | READY | Legal, Privacy, settings and SEO use the confirmed domains. |
| 巴黎 · 上海 · 香港 / Paris · Shanghai · Hong Kong | READY | Footer wording is consistent and does not claim three registered offices. |
| `contact@acoeursconsulting.com` | READY | Not present in current public templates or runtime source. |

No reliable repository evidence confirms a legal entity name, legal form, capital, registered office, SIREN, SIRET, RCS, RNE, intra-community VAT number, legal representative or publication director.

## 4. Legal Notice

Status: `READY` for pre-deployment structure; `NEEDS_LEGAL_COUNSEL` before publication.

The page contains brand, domains, contact information, content nature, intellectual property, external-link and regulated-service boundaries, and links to Privacy and Cookie policies. It contains no public TODO/TBC field and no claim that the Paris contact address is the registered office. The last-updated date is September 2026.

French and English legal text remain `REQUIRES_COUNSEL` internally. Missing statutory publisher and entity information is recorded in the legal handoff rather than exposed publicly.

## 5. Privacy Policy

Status: `READY` for technical accuracy; `NEEDS_LEGAL_COUNSEL` before publication.

Code and policy agree on the current contact data flow:

- Fields: `identity`, `organization_name`, `consultation_direction`, `subject`, `message`, `name`, `phone`, `email`, `preferred_language`, `contact_time`, `privacy_consent` and the `website` honeypot.
- Valid submissions are emailed; the website does not create a consultation database record.
- No CRM integration, file upload, public account, online purchase or online payment exists.
- Django Admin exists for framework administration, but no website content or inquiry model is registered.
- Hosting and application logs may process request metadata; provider, location and retention are deployment facts.
- The email recipient defaults to `info@acoeursconsulting.com`.

Legal basis, consent wording, retention, rights handling and transfer safeguards remain counsel items. The current privacy checkbox logic and wording were preserved.

## 6. Cookie Policy

Status: `READY` for current code; `NEEDS_DEPLOYMENT_FACT` after deployment.

Source and browser scans found no analytics, advertising pixels, tag manager, embedded maps/video, CAPTCHA, chat widget, `document.cookie`, application `localStorage` or application `sessionStorage`. Language selection uses the URL prefix and does not set a language preference cookie.

The contact form sets Django's necessary `csrftoken`; anonymous public browsing does not create `sessionid`. Admin authentication can create `sessionid`. No consent banner is implemented because no non-essential tracker is currently present. Production cookies and third-party requests must be rescanned after deployment.

## 7. Contact Form

Status: `READY`.

Verified controls:

- CSRF protection and server-side Django form validation
- hidden honeypot rejection
- phone or email required
- identity-to-direction validation
- length limits and `strip_tags` sanitisation for free-text fields
- required privacy field
- safe `Reply-To` only when a valid email is supplied
- configured recipient and sender defaults
- localized errors, send-failure handling and language-preserving success redirect
- POST/redirect/GET behavior prevents browser refresh from repeating a successful submission

Django's email classes reject newline-based header injection. User text is not written directly to raw SMTP headers.

## 8. Regulated-Service Language

Status: `READY` for the technical release; `NEEDS_LEGAL_COUNSEL` before publication.

The focused service pages state that accounting, tax, legal, litigation, notarial, lending, insurance, residency and other regulated work or decisions are performed by qualified professionals, authorities or financial institutions. Acoeurs is described as structuring needs, coordinating communication and following up projects.

Because headings and shorter cards still use terms such as law, accounting, banking, insurance, investment, tax and residency, counsel should confirm that the complete three-language presentation cannot imply that Acoeurs itself is the regulated provider.

## 9. B2C

Status: `NEEDS_LEGAL_COUNSEL`.

The website addresses companies, business owners, investors, individuals and families. It shows no public price, cart, online purchase, online payment or online contract flow; users can only submit a consultation request. Consumer withdrawal, pre-contract disclosures and mediation requirements have not been decided in the repository.

## 10. Marketing Claims

Status: `NEEDS_LEADERSHIP_CONFIRMATION`.

The homepage publishes:

- `10+` years of China–Europe service experience
- `500+` clients served
- `92%` success rate on key specialist engagements

The repository includes promotional source material but no auditable evidence set defining the measurement period, population, methodology or approval. These claims were not removed or altered.

## 11. Case Claims

Status: `NEEDS_LEADERSHIP_CONFIRMATION`.

The anonymous listed-company case states that valuable local contacts were established, visibility improved significantly, the project entered sustained progress and a systematic breakthrough was achieved. The repository does not contain client approval, substantiating records or an anonymity assessment. The same case appears on the homepage and Market Entry page.

## 12. Image Rights

Status: `NEEDS_LEADERSHIP_CONFIRMATION` and `NEEDS_LEGAL_COUNSEL`.

The current image inventory is maintained in the legal handoff. Client-owned provenance is documented for several photographs; Louvre/Sacré-Cœur/La Défense subject rights and people/venue considerations remain unassessed. The exact provenance of the brand mark, `home-about-team.webp`, `tax-legal.webp`, `business-growth.webp` and `personal-hero-paris-street.webp` is not established in `static/images/CREDITS.md`.

## 13. SEO

Status: `READY`.

- All 39 canonical pages self-canonicalize under the configured `SITE_URL`.
- Every canonical page exposes `zh-Hans`, `fr`, `en` and Chinese `x-default`.
- Sitemap contains exactly 39 canonical URLs and excludes redirects, Admin, health and error routes.
- `SITE_NOINDEX=True` produces `noindex, nofollow`, a global robots disallow and an empty sitemap with `X-Robots-Tag`.
- Open Graph title, description, type and canonical URL are present and localized.
- `og:image` is absent. This is a non-blocking publication enhancement, not a deployment blocker.

## 14. Security

Status: `READY`.

Production mode requires a non-development `SECRET_KEY`, rejects wildcard hosts, validates HTTPS CSRF origins and supports proxy HTTPS only through the explicit `SECURE_PROXY_SSL_HEADER_ENABLED` switch. SSL redirect, secure session/CSRF cookies, content-type sniffing protection, strict-origin referrer policy and frame denial have safe production defaults.

`SECURE_HSTS_SECONDS=0`, subdomain HSTS off and preload off are intentional for the first deployment. HSTS must be considered only after HTTPS, domain and redirect validation.

## 15. Secrets

Status: `FIXED_THIS_ROUND`.

The tracked-file scan found references to `SECRET_KEY` in `README.md`, `config/settings.py`, `render.yaml` and `website/tests.py`; these are documentation, environment loading, generated-value configuration and tests. No tracked private key, cloud credential, API key, SMTP password, database password or production secret value pattern was found.

`.env`, `.env.*`, common private-key/credential files, `db.sqlite3`, `staticfiles/`, virtual environments, Python caches, browser profiles, HAR files, temporary screenshot output and editor files are ignored. The browser/secret patterns were completed this round. Local ignored copies exist and are not tracked.

## 16. Database

Status: `READY`.

Local fallback is SQLite; `DATABASE_URL` enables PostgreSQL through `dj-database-url`. Migration checks report no model changes. Framework migrations are applied locally and the `website` app has no models or migrations. No production database was contacted.

## 17. Static Files

Status: `READY`.

WhiteNoise compressed manifest storage is available. Dry-run collection finds current CSS, JS, logo/favicon and image assets without writing tracked source. Browser smoke tests returned no static 404 response.

## 18. Dependencies

Status: `READY`.

`pip check` reports no broken requirements. `pip-audit` is not installed and was not added. Django remains pinned at the repository version; no dependency was upgraded. GNU gettext was installed in the local WSL tool environment so `compilemessages` could be verified.

## 19. Performance

Status: `READY` with non-blocking follow-up.

Hero assets are optimized WebP backgrounds except the homepage case illustration, which remains a 1.6 MB JPEG. Below-the-fold homepage `img` elements use lazy loading and decode asynchronously; CSS aspect-ratio containers limit layout shift. The largest referenced image is the 740 KB personal-services hero. No missing image or static request was observed.

Further image compression can be considered after visual approval; it is not required for the first gated deployment.

## 20. Accessibility

Status: `READY` for smoke-level review.

Rendered smoke pages have the correct `html lang`, one H1, visible Header/Footer, skip link, labeled form controls and no empty hash links. Header and Language menus support keyboard navigation, current language uses `aria-current`, and focus stays within the open submenu while tabbing through all three languages.

This was a quick technical audit, not a formal WCAG conformance assessment.

## 21. Links

Status: `FIXED_THIS_ROUND`.

Existing canonical page and CTA tests resolve all internal links. Error-page hardcoded root and unprefixed Contact links were replaced with Django URL names, so 400/403/404/500 pages now preserve the active language and their links resolve.

## 22. Third-party Resources

Status: `READY`.

No public template, CSS or JavaScript loads a remote font, CDN asset, analytics script, pixel, iframe, video, map, CAPTCHA, chat widget or API. Browser smoke requests used only the local test host. Mail and telephone links do not load third-party resources.

## 23. Multilingual Regression

Status: `READY`.

Smoke coverage used real Chrome at 1440×900 and 390×844 for the requested home, Contact, regulated-service, growth and Privacy URLs. All returned 200 with correct language, one H1, no horizontal overflow, no broken static requests and normal Header/Footer. FR/EN homepage About layouts did not overlap. Desktop pointer and keyboard Language flows and mobile menu expansion passed; same-page switching was preserved.

French and English catalogs contain no empty public translations or Chinese residue beyond approved brand/autonym content. Native-editor review remains recommended before publication.

## 24. Tests

| Command | Result |
|---|---|
| `manage.py check` | READY — no issues |
| `manage.py test website` | READY — 128 tests |
| `makemigrations --check --dry-run` | READY — no changes detected |
| `showmigrations` | READY — expected framework migrations applied |
| `compilemessages` | READY |
| `collectstatic --noinput --dry-run` | READY |
| `pip check` | READY — no broken requirements |
| `pip-audit` | NOT_APPLICABLE — not installed; not run |
| `check --deploy` | READY — only the intentional HSTS-not-enabled warning |
| `git diff --check` | READY |

## 25. Deployment Blockers

Status: `READY`.

No deployment blocker was found. Tests, migrations, static collection, runtime settings and routes are in a state suitable for a first gated production deployment.

## 26. Publication Blockers

Status: `BLOCKED`.

Public opening must wait for:

1. confirmed statutory entity and publisher information;
2. legal counsel review of Legal, Privacy, Cookie, consumer and regulated-service wording in all relevant languages;
3. leadership substantiation or withdrawal of marketing statistics;
4. leadership substantiation, client approval and anonymity review for case claims;
5. resolution of unknown or incomplete image provenance and rights;
6. deployment-fact completion and live privacy/Cookie/network verification;
7. native-editor review of French and English public copy;
8. explicit leadership and counsel approval to set `SITE_NOINDEX=False`.

## 27. Post-deployment Facts Required

Status: `NEEDS_DEPLOYMENT_FACT`.

Complete `POST_DEPLOYMENT_FACTS_CHECKLIST.md` with actual Hosting, DNS, database, email, logging, cookies, third-party requests and transfer facts. Verify both apex and `www`, HTTPS/proxy behavior, secure cookies, static assets, email delivery and access controls.

## 28. Legal Counsel Items

Status: `NEEDS_LEGAL_COUNSEL`.

The factual handoff is in `LEGAL_COUNSEL_HANDOFF_DRAFT.md`. It covers statutory identity, mentions légales, GDPR, B2C, regulated services, image/IP, marketing claims and case-study claims without proposing legal conclusions.

## First Production Deployment Gate

The next deployment must use:

- `SITE_NOINDEX=True`
- `SECURE_HSTS_SECONDS=0`
- `SECURE_HSTS_PRELOAD=False`
- an explicit production `SECRET_KEY`, hosts, CSRF origins, site URL and database URL
- Basic Auth, an IP allowlist or a maintenance gate where supported

The deployment is for private production verification only. It is not authorization to open the website to the public.
