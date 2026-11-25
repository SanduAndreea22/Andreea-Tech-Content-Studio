from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("packages/", views.packages, name="packages"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("portfolio/<int:pk>/", views.portfolio_detail, name="portfolio_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("contact/thanks/", views.contact_thanks, name="contact_thanks"),
]
