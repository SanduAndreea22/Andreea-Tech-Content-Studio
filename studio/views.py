from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm
from .models import SampleProject
from .packages import PACKAGE_GROUPS, REVISION_DAYS, TEXT_PRICE


def home(request):
    return render(request, "studio/home.html")


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


def free_sample(request):
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
        chosen = request.GET.get("package")
        for group in PACKAGE_GROUPS:
            for pack in group["packages"]:
                if pack["name"] == chosen:
                    initial["message"] = f"I'm interested in the {pack['name']} package (€{pack['price']})."
        form = ContactForm(initial=initial)
    return render(request, "studio/free_sample.html", {"form": form})


def free_sample_thanks(request):
    return render(request, "studio/free_sample_thanks.html")


def contact(request):
    return render(request, "studio/contact.html")


def privacy(request):
    return render(request, "studio/privacy.html")
