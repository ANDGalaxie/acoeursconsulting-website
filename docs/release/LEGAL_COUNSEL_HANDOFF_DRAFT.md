# Legal Counsel Handoff Draft

Prepared: 2026-09-15

Purpose: factual review checklist for leadership and legal counsel. This document is not a legal opinion and does not suggest the conclusion counsel should reach.

Status vocabulary: `READY`, `FIXED_THIS_ROUND`, `NEEDS_DEPLOYMENT_FACT`, `NEEDS_LEADERSHIP_CONFIRMATION`, `NEEDS_LEGAL_COUNSEL`, `BLOCKED`, `NOT_APPLICABLE`.

## A. Legal Entity

The public website currently identifies the brand as Acoeurs Consulting / 艾克斯咨询. Repository checklists describe the fields below as unconfirmed and no incorporation extract, registry record or equivalent reliable evidence was found.

| Fact | Existing public treatment | Question to confirm | Status |
|---|---|---|---|
| Legal entity name | Not published | Exact registered legal name | NEEDS_LEADERSHIP_CONFIRMATION |
| Legal form | Not published | Legal form and jurisdiction | NEEDS_LEADERSHIP_CONFIRMATION |
| Capital social | Not published | Amount and required presentation | NEEDS_LEADERSHIP_CONFIRMATION |
| Registered office / siège social | Not published | Confirm registered address | NEEDS_LEADERSHIP_CONFIRMATION |
| Paris address | Published as “Paris contact address” | Confirm continued public use; do not treat as registered office without evidence | NEEDS_LEADERSHIP_CONFIRMATION |
| SIREN | Not published | Registry number | NEEDS_LEADERSHIP_CONFIRMATION |
| SIRET | Not published | Establishment number | NEEDS_LEADERSHIP_CONFIRMATION |
| RCS | Not published | Registry city and number | NEEDS_LEADERSHIP_CONFIRMATION |
| RNE | Not published | Registration details if applicable | NEEDS_LEADERSHIP_CONFIRMATION |
| Intra-community VAT number | Not published as a company identifier | Number and publication requirement | NEEDS_LEADERSHIP_CONFIRMATION |
| Legal representative | Not published | Name, role and whether publication is required | NEEDS_LEADERSHIP_CONFIRMATION |
| Directeur de la publication | Not published | Identity and exact title | NEEDS_LEADERSHIP_CONFIRMATION |

## B. Mentions légales

Current public facts:

- Brand: Acoeurs Consulting / 艾克斯咨询
- Domains: `acoeursconsulting.com`, `www.acoeursconsulting.com`
- Email: `info@acoeursconsulting.com`
- Phones: `400-606-0685`, `+33 (0)9 72 96 05 73`
- Paris contact address: `32 AV. Kléber, 75116 Paris, France`
- Content/IP, external-link and regulated-service boundary paragraphs

| Existing treatment | Question to confirm | Status |
|---|---|---|
| Public page omits unknown statutory fields rather than showing TODO/TBC | Confirm required fields and approved values before publication | NEEDS_LEGAL_COUNSEL |
| Hosting provider is not named | Insert verified provider legal name, address and contact after deployment facts are known if required | NEEDS_LEGAL_COUNSEL |
| French legal notice translation | Review legal accuracy and French drafting | NEEDS_LEGAL_COUNSEL |
| English legal notice translation | Review legal accuracy and English drafting | NEEDS_LEGAL_COUNSEL |
| Address described only as a contact address | Confirm this description and whether another statutory address is required | NEEDS_LEGAL_COUNSEL |

Internal translation marker: French = `REQUIRES_COUNSEL`; English = `REQUIRES_COUNSEL`.

## C. Privacy / GDPR

Verified application facts:

- The contact form collects identity, optional organisation, consultation direction, optional subject/message, name, optional phone/email subject to one being required, preferred language, optional contact time, required privacy confirmation and a hidden honeypot.
- Valid submissions are sent by email to the configured recipient, defaulting to `info@acoeursconsulting.com`.
- No consultation record is written to the website database and no CRM or file upload is present.
- No public account, purchase or payment flow exists.
- Hosting/application logs may contain IP, request and technical information; live provider and retention facts are unknown.
- The website currently exposes `info@acoeursconsulting.com` for privacy requests.

| Existing wording / fact | Question to confirm | Status |
|---|---|---|
| Checkbox: user has read/agreed to the Privacy Policy and agrees to use of submitted information to handle the request | Decide whether consent is the appropriate basis and approve final three-language checkbox wording | NEEDS_LEGAL_COUNSEL |
| Policy lists legitimate interest, pre-contract contact measures and legal obligations as possible bases | Confirm basis per processing purpose | NEEDS_LEGAL_COUNSEL |
| Logs retained only as necessary; exact duration depends on deployment | Confirm provider logs, purposes and retention after deployment | NEEDS_DEPLOYMENT_FACT |
| Contact emails retained according to communication and record needs; no automatic deletion | Approve a retention schedule and operational deletion process | NEEDS_LEGAL_COUNSEL |
| Rights requests go to the general info mailbox | Confirm identity-verification, response and escalation procedure | NEEDS_LEGAL_COUNSEL |
| International transfer paragraph is conditional | Identify providers/regions, then confirm disclosures and safeguards | NEEDS_LEGAL_COUNSEL |
| Providers described generically | Insert verified recipients/processors and required details after deployment | NEEDS_DEPLOYMENT_FACT |
| CNIL complaint right included | Confirm final wording and links/details, if any | NEEDS_LEGAL_COUNSEL |
| French Privacy text | Legal and native-language review | NEEDS_LEGAL_COUNSEL |
| English Privacy text | Legal and native-language review | NEEDS_LEGAL_COUNSEL |

## D. Consumer / B2C

Facts:

- Personal Services addresses business owners, investors, individuals and families.
- No price, online checkout, payment, electronic contract or customer account appears.
- The only conversion flow is a contact request; service engagement occurs outside the website.
- No withdrawal-right workflow or consumer-mediation information is published.

| Question to confirm | Status |
|---|---|
| Which consumer pre-contract disclosures apply to the displayed personal services? | NEEDS_LEGAL_COUNSEL |
| Is a withdrawal-right notice/process required for later off-site contracting? | NEEDS_LEGAL_COUNSEL |
| Must a consumer mediator be designated and published? | NEEDS_LEGAL_COUNSEL |
| Does audience targeting require additional wording for investors, families or residency matters? | NEEDS_LEGAL_COUNSEL |

## E. Regulated Services

Current boundary wording says regulated decisions/work are performed by qualified professionals, authorities or financial institutions, while Acoeurs structures needs, coordinates information and follows projects.

| Page | Language | Existing wording / presentation | Reason for review | Status |
|---|---|---|---|---|
| Tax / Legal / Compliance | ZH/FR/EN | Accounting filings, tax treatment, legal opinions and litigation representation are performed by qualified professionals; Acoeurs coordinates | Confirm the overall page, service lists and metadata cannot imply Acoeurs is a law/accounting firm | NEEDS_LEGAL_COUNSEL |
| Company & Banking | ZH/FR/EN | Financial institutions decide account/credit outcomes; Acoeurs prepares and coordinates | Confirm banking, Fintech, payment and financing language does not imply regulated intermediation or guaranteed approval | NEEDS_LEGAL_COUNSEL |
| Personal Services | ZH/FR/EN | Authorities, financial institutions and qualified professionals independently handle residency, law, tax, notarial, lending and insurance matters | Confirm residency, investment, mortgage, insurance and tax descriptions and any required intermediary disclosures | NEEDS_LEGAL_COUNSEL |
| Homepage and overview cards | ZH/FR/EN | Short labels include law, accounting, banking, investment, insurance, tax and residency | Check shorter text in the context of linked boundary disclosures | NEEDS_LEGAL_COUNSEL |

Do not remove the service categories solely because they are regulated. Confirm the role description and any required qualification, partner or disclaimer language.

## F. Image / IP

Inventory is limited to images referenced by current public templates/CSS.

| Page/use | File | Source type | Source | Rights status / question | Status |
|---|---|---|---|---|---|
| Global brand/favicon | `static/images/branding/acoeurs-mark.svg` | UNKNOWN | Not documented in CREDITS | Confirm trademark/design ownership and web-use authorization | NEEDS_LEADERSHIP_CONFIRMATION |
| Homepage hero | `static/images/home/home-hero-la-defense.webp` | USER_OWNED_PHOTO | CREDITS says client/copyright holder | Confirm documented authorization and any La Défense architecture considerations | NEEDS_LEADERSHIP_CONFIRMATION |
| Homepage About | `static/images/home/home-about-team.webp` | UNKNOWN | CREDITS names a Pexels `about.jpg`, but does not link the deployed derivative | Confirm source file mapping, license record, people/model-release considerations | NEEDS_LEADERSHIP_CONFIRMATION |
| Homepage case | `static/images/case-study.jpg` | FREE_LICENSE_STOCK | Pexels photo 32845690, Sergey Sergeev | Preserve license evidence; confirm people/venue/trademark suitability and temporary-image decision | NEEDS_LEADERSHIP_CONFIRMATION |
| About hero | `static/images/about/about-hero-sacre-coeur.webp` | USER_OWNED_PHOTO | CREDITS says client/copyright holder | Confirm authorization and depicted-site/architecture considerations | NEEDS_LEADERSHIP_CONFIRMATION |
| Business overview hero | `static/images/services/enterprise-hero-cargo-ship.webp` | USER_OWNED_PHOTO | CREDITS says client/copyright holder | Confirm authorization and any vessel/trademark/venue issues | NEEDS_LEADERSHIP_CONFIRMATION |
| Market Entry hero | `static/images/services/details/market-entry.webp` | USER_OWNED_PHOTO | Client photo; Louvre noted | Review depicted-site/architecture and identifiable-person issues | NEEDS_LEGAL_COUNSEL |
| Company & Banking hero | `static/images/services/details/company-banking.webp` | USER_OWNED_PHOTO | Client photo; La Défense noted | Review depicted architecture/trademark issues | NEEDS_LEGAL_COUNSEL |
| Tax / Legal hero | `static/images/services/details/tax-legal.webp` | UNKNOWN | Not documented in CREDITS | Establish source and web-use rights | NEEDS_LEADERSHIP_CONFIRMATION |
| Local Operations hero | `static/images/services/details/local-operations.webp` | USER_OWNED_PHOTO | Client long-exposure Louvre photo | Review architecture/site and moving-visitor considerations | NEEDS_LEGAL_COUNSEL |
| Business Growth hero | `static/images/services/details/business-growth.webp` | UNKNOWN | Not documented in CREDITS | Establish source and web-use rights | NEEDS_LEADERSHIP_CONFIRMATION |
| Personal Services hero | `static/images/services/personal-hero-paris-street.webp` | UNKNOWN | Not documented in CREDITS | Establish source, people/venue/trademark and web-use rights | NEEDS_LEADERSHIP_CONFIRMATION |

## G. Marketing Claims

| Page | Language | Original / displayed claim | Evidence currently found | Question to confirm | Status |
|---|---|---|---|---|---|
| Homepage | ZH/FR/EN | `10+` years of China–Europe experience | Promotional source material only | Start date, scope, entity/team attribution and supporting records | NEEDS_LEADERSHIP_CONFIRMATION |
| Homepage | ZH/FR/EN | `500+` clients served | Promotional source material only | Definition of client, duplicate handling, period and supporting records | NEEDS_LEADERSHIP_CONFIRMATION |
| Homepage | ZH/FR/EN | `92%` success rate on key specialist engagements | Promotional source material only | Denominator, eligible services, success definition, measurement period and supporting records | NEEDS_LEADERSHIP_CONFIRMATION |

The claims were not removed or accepted as proven during this audit.

## H. Case-study Claims

The homepage and Market Entry page describe an anonymous Chinese listed-company engagement.

| Language | Original claim category | Existing wording | Question to confirm | Status |
|---|---|---|---|---|
| ZH/FR/EN | Client identity | “Chinese listed company” presented anonymously | Confirm the case is real, client-approved and sufficiently anonymized | NEEDS_LEADERSHIP_CONFIRMATION |
| ZH/FR/EN | Commercial relationships | High-value local contacts and partnerships were established | Identify evidence and approved level of specificity | NEEDS_LEADERSHIP_CONFIRMATION |
| ZH/FR/EN | Visibility | Market recognition and brand visibility improved significantly | Identify measurement or factual support | NEEDS_LEADERSHIP_CONFIRMATION |
| ZH/FR/EN | Progress | Project moved into sustained progress with an actionable growth path | Confirm timeframe, outcome and evidence | NEEDS_LEADERSHIP_CONFIRMATION |
| ZH/FR/EN | Breakthrough | “Systematic breakthrough” in the European market | Confirm whether this characterization is supportable and approved | NEEDS_LEADERSHIP_CONFIRMATION |
| Homepage image | ZH/FR/EN | Stock industrial-team illustration | Confirm the illustration cannot be mistaken for the client/team and retain the translated illustrative alt text | NEEDS_LEADERSHIP_CONFIRMATION |

## Counsel/Leadership Completion Record

| Area | Reviewer | Date | Decision / approved wording | Status |
|---|---|---|---|---|
| Legal entity | | | | BLOCKED |
| Mentions légales | | | | BLOCKED |
| Privacy / GDPR | | | | BLOCKED |
| Consumer / B2C | | | | BLOCKED |
| Regulated services | | | | BLOCKED |
| Image / IP | | | | BLOCKED |
| Marketing claims | | | | BLOCKED |
| Case-study claims | | | | BLOCKED |

Publication remains blocked until the required facts and approvals are recorded and leadership explicitly authorizes changing `SITE_NOINDEX=False`.
