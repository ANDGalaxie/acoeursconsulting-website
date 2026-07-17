# Acoeurs Consulting Website — Codex Instructions

## Project scope

This is the official corporate introduction website for Acoeurs Consulting.

Phase 1 includes only:

1. Django project foundation
2. Reusable global layout and design system
3. Fully implemented homepage
4. Styled placeholder pages and URL routes for future detail pages
5. Responsive desktop, tablet, and mobile layouts

Do not implement the full service detail content, CMS, payment, authentication,
customer accounts, or database-backed article management in Phase 1.

## Technology

- Python
- Django 5.2 LTS
- Django Templates
- Semantic HTML5
- Plain CSS
- Minimal vanilla JavaScript
- SQLite for local development
- No React
- No Vue
- No Tailwind
- No Bootstrap
- No external frontend framework
- No external CDN dependency
- Do not add a new package without explaining why it is needed

## Architecture

Use one Django app named `website`.

Use reusable templates:

- templates/base.html
- templates/includes/header.html
- templates/includes/footer.html
- templates/website/home.html
- templates/website/placeholder.html

Use static files:

- static/css/base.css
- static/css/components.css
- static/css/home.css
- static/js/main.js
- static/images/

Use CSS custom properties for the visual system.

## Design direction

The visual identity uses:

- Deep navy blue
- Champagne gold
- Warm white
- Light beige / warm gray

The website should feel:

- Professional
- International
- Calm
- Premium but not luxurious
- Modern
- Trustworthy
- Suitable for a strategy and execution consulting company

Avoid:

- Immigration-agency visual language
- Real-estate sales visual language
- Excessive gold
- Tourism imagery
- Logistics-heavy imagery
- Excessive animation
- Generic handshake imagery
- Crowded layouts

## Quality requirements

- Semantic HTML
- Keyboard-accessible navigation
- Visible focus states
- Alt text for meaningful images
- Respect `prefers-reduced-motion`
- No horizontal scrolling
- Mobile-first responsive behavior
- Reusable components
- Clear code comments where architecture is not obvious
- No inline CSS except where technically justified
- No duplicated large content blocks
- All internal links must resolve
- All placeholder pages must return HTTP 200

## Working rules

Before editing:

1. Inspect the existing repository.
2. Explain the implementation plan.
3. Identify files that will be created or modified.

After editing:

1. Run `python manage.py check`.
2. Run the test suite.
3. Report changed files.
4. Report commands executed.
5. Report any remaining limitations.
6. Do not make a Git commit unless explicitly instructed.

## Repository and production domain

GitHub owner:
ANDGalaxie

Recommended repository:
acoeursconsulting-website

Production domains:
- acoeursconsulting.com
- www.acoeursconsulting.com

Do not change DNS or deployment configuration during Phase 1.
Keep production host and HTTPS settings environment-driven.