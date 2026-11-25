# Putting the site online on PythonAnywhere (free account)

Do these steps after you create the new account. Replace `YOURUSER` with your PythonAnywhere username.

## 1. Get the code
In a **Bash console** on PythonAnywhere:

```bash
git clone https://github.com/SanduAndreea22/Andreea-Tech-Content-Studio.git
cd Andreea-Tech-Content-Studio
git checkout claude/eager-archimedes-vbhxw5
python3.13 -m venv ~/.virtualenvs/studio
source ~/.virtualenvs/studio/bin/activate
pip install -r requirements.txt
```

(If Python 3.13 is not offered on your account, use the newest version you have, at least 3.10.)

## 2. Secret values
Generate a secret key and keep it:

```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

In the **Web** tab, open the WSGI configuration file and add these lines **above** the Django lines:

```python
import os
os.environ["DJANGO_SECRET_KEY"] = "PASTE-THE-KEY-HERE"
os.environ["DJANGO_ALLOWED_HOSTS"] = "YOURUSER.pythonanywhere.com"
os.environ["DJANGO_CSRF_TRUSTED_ORIGINS"] = "https://YOURUSER.pythonanywhere.com"
os.environ["DJANGO_ADMIN_URL"] = "pick-a-secret-word/"   # your admin address, not /admin/
# Optional. Email and LinkedIn are already set in config/settings.py.
# Add these lines only to change them or to show Instagram / Facebook (empty means hidden):
# os.environ["SITE_INSTAGRAM"] = "https://www.instagram.com/..."
# os.environ["SITE_FACEBOOK"] = "https://www.facebook.com/..."
```

The rest of the WSGI file should point to the project:

```python
import sys
path = "/home/YOURUSER/Andreea-Tech-Content-Studio"
if path not in sys.path:
    sys.path.insert(0, path)
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Never commit the secret key to GitHub.

## 3. Database and admin user
Back in the Bash console, with the same environment values set for this shell:

```bash
export DJANGO_SECRET_KEY="PASTE-THE-KEY-HERE"
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

Use a long password (10+ characters, not a common one).

## 4. Web tab settings
- **Source code / Working directory:** `/home/YOURUSER/Andreea-Tech-Content-Studio`
- **Virtualenv:** `/home/YOURUSER/.virtualenvs/studio`
- **Static files** (two rows):
  - URL `/static/` → directory `/home/YOURUSER/Andreea-Tech-Content-Studio/staticfiles`
  - URL `/media/` → directory `/home/YOURUSER/Andreea-Tech-Content-Studio/media`
- **Force HTTPS:** on.

Press **Reload**. The site is at `https://YOURUSER.pythonanywhere.com`.

## 5. Every day use
- Messages: `https://YOURUSER.pythonanywhere.com/<your-admin-word>/` → **Messages**. Set the status to New / Ad sent / Replied.
- Portfolio PDFs: same admin → **Sample projects** → Add (PDF up to 10 MB). You can also add a **Cover** picture (JPG, PNG or WebP, up to 5 MB, for example the first page of the PDF). It is shown on the card.
- Prices and package lists: edit `studio/packages.py`, then pull and Reload.

## Deleting old messages (twice a year)
The Privacy page says messages are kept for up to 12 months. In the Bash console, with the virtualenv active and the secret key exported:

```bash
python manage.py delete_old_requests          # shows how many are older than 12 months
python manage.py delete_old_requests --yes    # deletes them
```

## Appearing on Google
The site already has `sitemap.xml` and `robots.txt`. To tell Google it exists:
1. Go to https://search.google.com/search-console and add a property of type **URL prefix** with `https://YOURUSER.pythonanywhere.com/`.
2. Choose the **HTML tag** verification method. Google shows a tag like `<meta name="google-site-verification" content="CODE">`. Copy only the CODE.
3. In the WSGI file (Web tab) add `os.environ["GOOGLE_SITE_VERIFICATION"] = "CODE"` above the Django lines, save, and press **Reload**. Then press **Verify** in Search Console.
4. In Search Console, open **Sitemaps** and add `sitemap.xml`.
5. Open **URL inspection**, paste the home page address and press **Request indexing**.

It usually takes a few days to a few weeks to appear. Searching for `site:YOURUSER.pythonanywhere.com` on Google shows which pages are already known.

## 6. Free account reminders
- Press **Run until 3 months from today** in the Web tab every 3 months, or the site stops.
- Back up `db.sqlite3` and the `media/` folder from time to time (download them from the Files tab). They hold your messages and PDFs and are not in GitHub.

## Updating the site later
```bash
cd ~/Andreea-Tech-Content-Studio
git pull
source ~/.virtualenvs/studio/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```
Then press **Reload** in the Web tab.
