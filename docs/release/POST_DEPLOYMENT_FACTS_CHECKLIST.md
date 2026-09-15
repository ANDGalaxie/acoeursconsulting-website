# Post-deployment Facts Checklist

Complete this checklist against the live gated production environment. Do not infer values from local settings, a deployment template or vendor marketing material.

Status vocabulary: `READY`, `FIXED_THIS_ROUND`, `NEEDS_DEPLOYMENT_FACT`, `NEEDS_LEADERSHIP_CONFIRMATION`, `NEEDS_LEGAL_COUNSEL`, `BLOCKED`, `NOT_APPLICABLE`.

## Release Gate

| Check | Status | Verified value / evidence |
|---|---|---|
| `SITE_NOINDEX=True` in live environment | NEEDS_DEPLOYMENT_FACT | |
| Live HTML emits `noindex, nofollow` | NEEDS_DEPLOYMENT_FACT | |
| Live `robots.txt` returns global `Disallow: /` | NEEDS_DEPLOYMENT_FACT | |
| Live sitemap is empty while gated | NEEDS_DEPLOYMENT_FACT | |
| Basic Auth, IP allowlist or maintenance gate | NEEDS_DEPLOYMENT_FACT | Record mechanism or `NOT_APPLICABLE` with reason. |
| Public-launch approval | BLOCKED | Leadership and legal approval required before changing `SITE_NOINDEX`. |

## Hosting

| Fact | Status | Actual value / evidence |
|---|---|---|
| Provider | NEEDS_DEPLOYMENT_FACT | |
| Provider legal name | NEEDS_DEPLOYMENT_FACT | |
| Provider address | NEEDS_DEPLOYMENT_FACT | |
| Provider phone/contact channel | NEEDS_DEPLOYMENT_FACT | |
| Hosting country | NEEDS_DEPLOYMENT_FACT | |
| Service region / data center | NEEDS_DEPLOYMENT_FACT | |
| Service plan | NEEDS_DEPLOYMENT_FACT | |
| Runtime Python and dependency versions | NEEDS_DEPLOYMENT_FACT | |
| HTTPS termination point | NEEDS_DEPLOYMENT_FACT | |
| Processor agreement / DPA availability | NEEDS_DEPLOYMENT_FACT | |

## Domain and DNS

| Fact | Status | Actual value / evidence |
|---|---|---|
| Registrar | NEEDS_DEPLOYMENT_FACT | |
| DNS provider | NEEDS_DEPLOYMENT_FACT | |
| CDN / reverse proxy | NEEDS_DEPLOYMENT_FACT | |
| Apex `acoeursconsulting.com` behavior | NEEDS_DEPLOYMENT_FACT | |
| `www.acoeursconsulting.com` behavior | NEEDS_DEPLOYMENT_FACT | |
| Canonical host and redirect direction | NEEDS_DEPLOYMENT_FACT | |
| TLS certificate issuer and validity | NEEDS_DEPLOYMENT_FACT | |
| DNSSEC status | NEEDS_DEPLOYMENT_FACT | |
| Domain auto-renewal owner/process | NEEDS_LEADERSHIP_CONFIRMATION | |

## Database

| Fact | Status | Actual value / evidence |
|---|---|---|
| Provider | NEEDS_DEPLOYMENT_FACT | |
| Database engine and version | NEEDS_DEPLOYMENT_FACT | |
| Region / country | NEEDS_DEPLOYMENT_FACT | |
| Encryption in transit | NEEDS_DEPLOYMENT_FACT | |
| Encryption at rest | NEEDS_DEPLOYMENT_FACT | |
| Backup enabled | NEEDS_DEPLOYMENT_FACT | |
| Backup frequency and retention | NEEDS_DEPLOYMENT_FACT | |
| Restore procedure tested | NEEDS_DEPLOYMENT_FACT | |
| Access roles | NEEDS_DEPLOYMENT_FACT | |
| Current website inquiry data stored | READY | None in application models; reconfirm deployed code. |

## Email

| Fact | Status | Actual value / evidence |
|---|---|---|
| Mailbox provider | NEEDS_DEPLOYMENT_FACT | |
| SMTP / transactional provider | NEEDS_DEPLOYMENT_FACT | |
| Provider legal name | NEEDS_DEPLOYMENT_FACT | |
| Processing region / country | NEEDS_DEPLOYMENT_FACT | |
| Sender address | NEEDS_DEPLOYMENT_FACT | |
| Contact recipient | NEEDS_DEPLOYMENT_FACT | |
| Successful form delivery | NEEDS_DEPLOYMENT_FACT | Use a controlled test submission. |
| Failure handling / alerting | NEEDS_DEPLOYMENT_FACT | |
| SPF | NEEDS_DEPLOYMENT_FACT | |
| DKIM | NEEDS_DEPLOYMENT_FACT | |
| DMARC | NEEDS_DEPLOYMENT_FACT | |
| Mailbox retention and deletion process | NEEDS_DEPLOYMENT_FACT | |
| Processor agreement / DPA | NEEDS_DEPLOYMENT_FACT | |

## Logs

| Fact | Status | Actual value / evidence |
|---|---|---|
| Web access logs enabled | NEEDS_DEPLOYMENT_FACT | |
| Application logs enabled | NEEDS_DEPLOYMENT_FACT | |
| IP address captured | NEEDS_DEPLOYMENT_FACT | |
| User agent / request path captured | NEEDS_DEPLOYMENT_FACT | |
| Log region / country | NEEDS_DEPLOYMENT_FACT | |
| Retention period | NEEDS_DEPLOYMENT_FACT | |
| Authorized access roles | NEEDS_DEPLOYMENT_FACT | |
| Export / deletion process | NEEDS_DEPLOYMENT_FACT | |
| Error monitoring service | NEEDS_DEPLOYMENT_FACT | |

## Cookies and Browser Storage

Record each actual cookie separately.

| Name | Status | Purpose | Lifetime | First/third party | Domain/path | Secure | HttpOnly | SameSite |
|---|---|---|---|---|---|---|---|---|
| `csrftoken` | NEEDS_DEPLOYMENT_FACT | | | | | | | |
| `sessionid` if created | NEEDS_DEPLOYMENT_FACT | | | | | | | |
| Other cookies | NEEDS_DEPLOYMENT_FACT | | | | | | | |

| Browser storage / behavior | Status | Actual value / evidence |
|---|---|---|
| Language preference cookie absent | NEEDS_DEPLOYMENT_FACT | |
| `localStorage` keys | NEEDS_DEPLOYMENT_FACT | |
| `sessionStorage` keys | NEEDS_DEPLOYMENT_FACT | |
| Cookies before Contact/Admin use | NEEDS_DEPLOYMENT_FACT | |
| Cookies after Contact page visit | NEEDS_DEPLOYMENT_FACT | |
| Cookies after Admin authentication | NEEDS_DEPLOYMENT_FACT | |
| Consent banner required by actual live behavior | NEEDS_LEGAL_COUNSEL | Review only after live scan. |

## Third-party Network Requests

Use browser DevTools or an automated HAR against representative pages in all three languages.

| Fact | Status | Actual value / evidence |
|---|---|---|
| All contacted domains | NEEDS_DEPLOYMENT_FACT | |
| Fonts / CDN requests | NEEDS_DEPLOYMENT_FACT | |
| Analytics / tag manager | NEEDS_DEPLOYMENT_FACT | |
| Advertising pixels | NEEDS_DEPLOYMENT_FACT | |
| Embedded media / maps | NEEDS_DEPLOYMENT_FACT | |
| CAPTCHA / chat widgets | NEEDS_DEPLOYMENT_FACT | |
| Error monitoring | NEEDS_DEPLOYMENT_FACT | |
| Provider purpose | NEEDS_DEPLOYMENT_FACT | |
| Cookie / tracking behavior | NEEDS_DEPLOYMENT_FACT | |
| Personal-data implication | NEEDS_DEPLOYMENT_FACT | |
| Can be self-hosted | NEEDS_DEPLOYMENT_FACT | |

## International Transfers

| Fact | Status | Actual value / evidence |
|---|---|---|
| Hosting data remains in EEA | NEEDS_DEPLOYMENT_FACT | |
| Database data remains in EEA | NEEDS_DEPLOYMENT_FACT | |
| Email data remains in EEA | NEEDS_DEPLOYMENT_FACT | |
| Logs remain in EEA | NEEDS_DEPLOYMENT_FACT | |
| Non-EEA recipients/providers | NEEDS_DEPLOYMENT_FACT | |
| Unknown provider subprocessors | NEEDS_DEPLOYMENT_FACT | |
| Transfer mechanism / safeguard | NEEDS_LEGAL_COUNSEL | Determine after providers and regions are known. |

## Live Technical Verification

| Check | Status | Evidence |
|---|---|---|
| `/health/` HTTP 200 | NEEDS_DEPLOYMENT_FACT | |
| CSS, JS, logo, favicon and all images HTTP 200 | NEEDS_DEPLOYMENT_FACT | |
| No mixed content | NEEDS_DEPLOYMENT_FACT | |
| Apex and `www` redirects are intentional | NEEDS_DEPLOYMENT_FACT | |
| `ALLOWED_HOSTS` correct | NEEDS_DEPLOYMENT_FACT | |
| `CSRF_TRUSTED_ORIGINS` correct | NEEDS_DEPLOYMENT_FACT | |
| `SECURE_PROXY_SSL_HEADER_ENABLED` matches proxy behavior | NEEDS_DEPLOYMENT_FACT | |
| Secure cookie flags under HTTPS | NEEDS_DEPLOYMENT_FACT | |
| Contact form CSRF and SMTP delivery | NEEDS_DEPLOYMENT_FACT | |
| 400/403/404/500 pages do not leak internals | NEEDS_DEPLOYMENT_FACT | |
| Canonical and hreflang use the final preferred host | NEEDS_DEPLOYMENT_FACT | |
| HSTS remains disabled during initial validation | NEEDS_DEPLOYMENT_FACT | |

## Legal and Publication Follow-up

| Item | Status | Evidence / owner |
|---|---|---|
| Hosting/DB/email/log facts copied into Privacy Policy | NEEDS_LEGAL_COUNSEL | |
| Actual Cookie table reconciled | NEEDS_LEGAL_COUNSEL | |
| International transfers reconciled | NEEDS_LEGAL_COUNSEL | |
| Legal entity and publisher facts inserted | NEEDS_LEADERSHIP_CONFIRMATION | |
| French legal text approved | NEEDS_LEGAL_COUNSEL | |
| English legal text approved | NEEDS_LEGAL_COUNSEL | |
| Marketing claims substantiated | NEEDS_LEADERSHIP_CONFIRMATION | |
| Case claims and anonymity approved | NEEDS_LEADERSHIP_CONFIRMATION | |
| Image provenance and rights cleared | NEEDS_LEADERSHIP_CONFIRMATION | |
| Native French/English editorial review | NEEDS_LEADERSHIP_CONFIRMATION | |
| Publication blockers reduced to zero | BLOCKED | |
| Explicit approval to set `SITE_NOINDEX=False` | BLOCKED | |
