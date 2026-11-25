from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("services/", views.services, name="services"),
    path("packages/", views.packages, name="packages"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("portfolio/<int:pk>/", views.portfolio_detail, name="portfolio_detail"),
    path("about/", views.about, name="about"),
    path("free-sample/", views.free_sample, name="free_sample"),
    path("free-sample/thanks/", views.free_sample_thanks, name="free_sample_thanks"),
    path("contact/", views.contact, name="contact"),
    path("privacy/", views.privacy, name="privacy"),
]
