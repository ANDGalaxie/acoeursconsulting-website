# Acoeurs Consulting Website

Phase 1 Django project skeleton for the Acoeurs Consulting corporate introduction website.

## Stack

- Python
- Django 5.2
- Django Templates
- Plain CSS
- Minimal vanilla JavaScript

## Structure

- `config/`: Django project configuration
- `website/`: single website app with views, URLs, and tests
- `templates/`: shared layout, homepage, and placeholder pages
- `static/`: CSS, JavaScript, and local images
- `docs/`: project specifications

## Local development

```bash
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

## Current phase

This repository currently contains the Django foundation, shared layout shell, homepage stub, placeholder pages, and route coverage tests. The full homepage visual implementation is intentionally deferred.
