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
os.environ["SITE_EMAIL"] = ""        # shown on the site if filled in
os.environ["SITE_INSTAGRAM"] = ""
os.environ["SITE_FACEBOOK"] = ""
os.environ["SITE_LINKEDIN"] = ""
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
- Messages: `https://YOURUSER.pythonanywhere.com/<your-admin-word>/` → **Messages**. Set the status to New / Sample sent / Replied.
- Portfolio PDFs: same admin → **Sample projects** → Add (PDF up to 10 MB).
- Prices and package lists: edit `studio/packages.py`, then pull and Reload.

## 6. Free account reminders
- Press **Run until 3 months from today** in the Web tab every 3 months, or the site stops.
- Back up `db.sqlite3` and the `media/` folder from time to time (download them from the Files tab). They hold your messages and PDFs and are not in GitHub.

## Updating the site later
```bash
cd ~/Andreea-Tech-Content-Studio
git pull
source ~/.virtualenvs/studio/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```
Then press **Reload** in the Web tab.
