# Andreea Sandu: website

Site for Andreea Sandu, Copywriter & Social Media Content Creator. Django, SQLite, English pages.

- Pages: Home, Services, Packages, Portfolio (PDF samples), About, Contact (free sample request form).
- Messages and portfolio PDFs are managed in the Django admin.
- Brand sheet, assets and mock: `brand/`.
- Putting it online on PythonAnywhere: `DEPLOY.md`.

## Run it on your computer

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_DEBUG=1
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Tests

```bash
DJANGO_DEBUG=1 python manage.py test
```
