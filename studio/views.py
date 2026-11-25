from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm
from .models import SampleProject
from .packages import PACKAGE_GROUPS


def home(request):
    return render(request, "studio/home.html")


def services(request):
    return render(request, "studio/services.html")


def packages(request):
    return render(request, "studio/packages.html", {"groups": PACKAGE_GROUPS})


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


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contact_thanks")
    else:
        initial = {}
        service = request.GET.get("service")
        if service in dict(ContactForm.Meta.model.SERVICE_CHOICES):
            initial["service"] = service
        form = ContactForm(initial=initial)
    return render(request, "studio/contact.html", {"form": form})


def contact_thanks(request):
    return render(request, "studio/contact_thanks.html")
