# Acoeurs Consulting Website

Phase 1 Django project for the Acoeurs Consulting corporate introduction website.

## Stack

- Python 3.12
- Django 5.2
- Django Templates
- Plain CSS
- Minimal vanilla JavaScript
- SQLite for local fallback
- PostgreSQL for Render production
- Gunicorn
- WhiteNoise

## Project Structure

- `config/`: Django project configuration
- `website/`: single app with homepage, placeholders, health endpoint, and tests
- `templates/`: shared layout, homepage, placeholders, and error pages
- `static/`: CSS, JavaScript, local images, and brand assets
- `docs/`: project specifications

## Local Development

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Start the dev server:

```bash
python manage.py runserver
```

Local development defaults:

- `DEBUG=True`
- SQLite database at `db.sqlite3`
- allowed hosts: `localhost`, `127.0.0.1`

## Environment Variables

The application supports these environment variables:

- `SECRET_KEY`
  - Required when `DEBUG=False`
  - Optional in local development
- `DEBUG`
  - Boolean string: `True` / `False`
- `ALLOWED_HOSTS`
  - Comma-separated hosts
  - Also accepted as `DJANGO_ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
  - Comma-separated origins including scheme
  - Also accepted as `DJANGO_CSRF_TRUSTED_ORIGINS`
- `SITE_URL`
  - Primary absolute site URL used for canonical generation
  - Leave unset in local development if you do not want canonical tags
- `SITE_NOINDEX`
  - Boolean string used to emit `noindex, nofollow` on staging or private environments
- `DATABASE_URL`
  - PostgreSQL connection string for Render production
- `SECURE_SSL_REDIRECT`
  - Boolean string
- `SECURE_HSTS_SECONDS`
  - Integer, default `0`

Render also provides `RENDER_EXTERNAL_HOSTNAME`, which the settings append to accepted hosts and trusted origins when present.

## Local SQLite and Production PostgreSQL

Database selection is automatic:

- If `DATABASE_URL` is set, Django uses PostgreSQL.
- If `DATABASE_URL` is missing, Django falls back to SQLite.

This keeps local development simple while allowing Render PostgreSQL in production.

## Static Files

Production static file behavior:

- `STATIC_ROOT` is `staticfiles/`
- `collectstatic --noinput` is required during build
- WhiteNoise is configured immediately after `SecurityMiddleware`
- Django `STORAGES` uses compressed, hashed static files in production-capable environments

If deployment dependencies are not installed in the local environment, the project falls back to Django static file storage so local checks can still run.

## Render Deployment

### Render Blueprint Files

- `render.yaml`
- `build.sh`

### Build Command

```bash
./build.sh
```

`build.sh` runs:

1. `python manage.py collectstatic --noinput`
2. `python manage.py migrate --noinput`

### Start Command

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

### Render Services

`render.yaml` defines:

- one Django web service
- one PostgreSQL database
- generated `SECRET_KEY`
- production `DEBUG=False`
- default domain-related environment variables
- database connection wiring through `DATABASE_URL`
- health check path `/health/`

## Render Setup Steps

1. Push the repository to GitHub:
   - `ANDGalaxie/acoeursconsulting-website`
2. In Render, create a Blueprint deployment from the repository.
3. Review the generated web service and PostgreSQL database.
4. Confirm or adjust service plans in the Render Dashboard.
5. Verify environment variables before the first deploy.
6. Deploy and wait for:
   - build success
   - migrations success
   - `/health/` returning HTTP 200

## Domain Configuration

### Staging

Bind:

- `staging.acoeursconsulting.com`

Recommended environment values:

- `ALLOWED_HOSTS=staging.acoeursconsulting.com`
- `CSRF_TRUSTED_ORIGINS=https://staging.acoeursconsulting.com`
- `SITE_URL=https://staging.acoeursconsulting.com`
- `SITE_NOINDEX=True`

The Render runtime hostname is automatically added when `RENDER_EXTERNAL_HOSTNAME` is present.

### Production

Bind:

- `acoeursconsulting.com`
- `www.acoeursconsulting.com`

Recommended environment values:

- `ALLOWED_HOSTS=acoeursconsulting.com,www.acoeursconsulting.com`
- `CSRF_TRUSTED_ORIGINS=https://acoeursconsulting.com,https://www.acoeursconsulting.com`
- `SITE_URL=https://acoeursconsulting.com`
- `SITE_NOINDEX=False`

If the same Render service temporarily serves both staging and production-style hostnames, you can include all required domains in the same environment variable. The Render runtime hostname will still be appended automatically.

## HTTPS and HSTS Rollout

The project is prepared for HTTPS behind Render:

- `SECURE_PROXY_SSL_HEADER` is configured
- `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` are enabled in production mode
- `SECURE_SSL_REDIRECT` is environment-driven
- `SECURE_HSTS_SECONDS` is environment-driven and defaults to `0`

Recommended rollout:

1. First deploy with `SECURE_HSTS_SECONDS=0`
2. Verify HTTPS, cookies, redirects, and canonical domains
3. Increase HSTS gradually after validation

Do not enable long-lived HSTS preload until staging and production behavior are fully confirmed.

## Health Check

Health endpoint:

- `GET /health/`
- Returns HTTP 200
- Returns simple JSON: `{"status": "ok"}`

## Error Pages

Custom templates are provided for:

- `400.html`
- `403.html`
- `404.html`
- `500.html`

These pages:

- use the existing brand layout
- avoid database access
- provide a clear route back to the homepage

## Post-Deploy Checklist

After each staging or production deploy, verify:

1. Homepage loads correctly
2. CSS, JS, logo, and images load under `DEBUG=False`
3. `/health/` returns HTTP 200
4. Placeholder pages return HTTP 200
5. Admin can load if enabled for operational use
6. HTTPS redirect behaves correctly
7. Cookies are marked secure in production
8. `acoeursconsulting.com` and `www.acoeursconsulting.com` are both accepted
9. `staging.acoeursconsulting.com` is accepted if bound
10. No mixed-content errors appear in the browser

## Rollback

If a deploy fails:

1. Open the Render service
2. Select the last healthy deploy
3. Roll back to that deploy in the Dashboard
4. Review:
   - environment variables
   - build logs
   - migration output
   - static file manifest issues

If the failure was caused by a configuration change, restore the previous environment values first, then redeploy.
