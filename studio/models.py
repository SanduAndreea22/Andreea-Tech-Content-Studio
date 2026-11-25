from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

import os
import uuid

MAX_PDF_BYTES = 10 * 1024 * 1024


def sample_upload_path(instance, filename):
    """Random file name, so the address of a hidden (unpublished) PDF cannot be guessed."""
    return f"samples/{uuid.uuid4().hex}.pdf"


MAX_COVER_BYTES = 5 * 1024 * 1024


def sample_cover_path(instance, filename):
    """Random file name for the optional cover picture (keeps the picture's own extension)."""
    extension = os.path.splitext(filename)[1].lower()
    return f"samples/covers/{uuid.uuid4().hex}{extension}"


def validate_cover_size(file):
    if file.size > MAX_COVER_BYTES:
        raise ValidationError("The picture must be 5 MB or smaller.")


def validate_pdf(file):
    """Accept only real PDFs up to 10 MB (checks the file header, not just the name)."""
    if file.size > MAX_PDF_BYTES:
        raise ValidationError("The PDF must be 10 MB or smaller.")
    header = file.read(5)
    file.seek(0)
    if header != b"%PDF-":
        raise ValidationError("This file is not a valid PDF.")


class ContactRequest(models.Model):
    SERVICE_CHOICES = [
        ("ads", "Ads"),
        ("posts", "Social media posts"),
        ("texts", "Product, service & event texts"),
        ("unsure", "Not sure yet"),
    ]
    STATUS_CHOICES = [
        ("new", "New"),
        ("sample_sent", "Ad sent"),
        ("replied", "Replied"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    business_name = models.CharField(max_length=150)
    service = models.CharField(max_length=10, choices=SERVICE_CHOICES, default="unsure")
    what_you_sell = models.TextField("What they sell, and to whom", max_length=1000)
    link = models.CharField("Instagram, Facebook or website", max_length=300, blank=True)
    goal = models.CharField("What they want to achieve", max_length=300, blank=True)
    message = models.TextField(max_length=2000, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="new", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "message"

    def __str__(self):
        return f"{self.business_name} ({self.name})"


class SampleProject(models.Model):
    CATEGORY_CHOICES = [
        ("ad", "Ad"),
        ("posts", "Social posts"),
        ("carousel", "Carousel"),
        ("reels", "Reels script"),
    ]

    title = models.CharField(max_length=120)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    description = models.CharField(
        max_length=240,
        help_text="One short line: who the example business is and what the sample shows.",
    )
    pdf = models.FileField(
        upload_to=sample_upload_path,
        validators=[FileExtensionValidator(["pdf"]), validate_pdf],
    )
    cover = models.ImageField(
        upload_to=sample_cover_path,
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), validate_cover_size],
        help_text="Optional picture shown on the card, for example the first page of the PDF. JPG, PNG or WebP, up to 5 MB. Best size: 1200 x 900 px (4:3). Other shapes are cropped.",
    )
    is_published = models.BooleanField(default=True, help_text="Untick to hide it from the site.")
    sort_order = models.PositiveIntegerField(default=0, help_text="Lower numbers come first.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = "sample project"

    def __str__(self):
        return self.title
