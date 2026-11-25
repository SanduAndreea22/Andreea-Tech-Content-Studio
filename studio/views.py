import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse

from .forms import ContactForm
from .models import SampleProject
from .packages import PACKAGE_GROUPS, REVISION_DAYS, TEXT_PRICE


def home(request):
    links = {key: value for key, value in settings.SITE_LINKS.items() if value}
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": settings.SITE_NAME,
        "jobTitle": settings.SITE_TAGLINE,
        "url": request.build_absolute_uri(reverse("home")),
        "image": request.build_absolute_uri(static("studio/img/hero-portrait.webp")),
    }
    if links.get("email"):
        data["email"] = links["email"]
    same_as = [links[key] for key in ("linkedin", "instagram", "facebook") if links.get(key)]
    if same_as:
        data["sameAs"] = same_as
    # "<" is escaped so the data can never close the script tag.
    return render(request, "studio/home.html", {"json_ld": json.dumps(data).replace("<", "\\u003c")})


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /free-sample/thanks/",
        f"Sitemap: {request.build_absolute_uri(reverse('sitemap'))}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


def _cheapest(group_title):
    for group in PACKAGE_GROUPS:
        if group["title"] == group_title:
            return min(pack["price"] for pack in group["packages"])


def services(request):
    return render(request, "studio/services.html", {
        "ads_from": _cheapest("Ads"),
        "posts_from": _cheapest("Social media posts"),
        "groups": PACKAGE_GROUPS,
        "revision_days": REVISION_DAYS,
        "text_price": TEXT_PRICE,
        "days_min": min(p["days"] for g in PACKAGE_GROUPS for p in g["packages"]),
        "days_max": max(p["days"] for g in PACKAGE_GROUPS for p in g["packages"]),
    })


def packages(request):
    return render(request, "studio/packages.html", {"groups": PACKAGE_GROUPS, "text_price": TEXT_PRICE})


def portfolio(request):
    category = request.GET.get("category", "")
    valid = dict(SampleProject.CATEGORY_CHOICES)
    samples = SampleProject.objects.filter(is_published=True)
    if category in valid:
        samples = samples.filter(category=category)
    else:
        category = ""
    return render(request, "studio/portfolio.html", {
        "samples": samples,
        "categories": SampleProject.CATEGORY_CHOICES,
        "active_category": category,
    })


def portfolio_detail(request, pk):
    sample = get_object_or_404(SampleProject, pk=pk, is_published=True)
    return render(request, "studio/portfolio_detail.html", {"sample": sample})


def about(request):
    return render(request, "studio/about.html")


def _chosen_package(request):
    """The package picked on the Packages page (from the address), or None."""
    chosen = request.GET.get("package")
    for group in PACKAGE_GROUPS:
        for pack in group["packages"]:
            if pack["name"] == chosen:
                return pack
    return None


def free_sample(request):
    package = _chosen_package(request)
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("free_sample_thanks")
    else:
        initial = {}
        service = request.GET.get("service")
        if service in dict(ContactForm.Meta.model.SERVICE_CHOICES):
            initial["service"] = service
        # A package button on the Packages page pre-fills the message with the chosen package.
        if package:
            initial["message"] = f"I'm interested in the {package['name']} package (€{package['price']})."
        form = ContactForm(initial=initial)
    return render(request, "studio/free_sample.html", {"form": form, "package": package})


def free_sample_thanks(request):
    return render(request, "studio/free_sample_thanks.html")


def contact(request):
    return render(request, "studio/contact.html")


def privacy(request):
    return render(request, "studio/privacy.html")
