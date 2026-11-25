from django.conf import settings


def site(request):
    links = {key: value for key, value in settings.SITE_LINKS.items() if value}
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_TAGLINE": settings.SITE_TAGLINE,
        "SITE_LINKS": links,
    }
