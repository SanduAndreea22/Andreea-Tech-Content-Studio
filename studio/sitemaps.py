from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import SampleProject


class PagesSitemap(Sitemap):
    """The public pages. The form's thank-you page and the admin are left out on purpose."""
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ["home", "services", "packages", "portfolio", "about", "contact", "privacy"]

    def location(self, name):
        return reverse(name)


class SamplesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return SampleProject.objects.filter(is_published=True)

    def location(self, sample):
        return reverse("portfolio_detail", args=[sample.pk])

    def lastmod(self, sample):
        return sample.created_at
