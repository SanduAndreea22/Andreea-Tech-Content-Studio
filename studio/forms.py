from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import ContactRequest


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)

    # Honeypot: hidden from people, filled in by simple bots.
    # The name is deliberately not "website", "url" or "phone", which browsers autofill.
    hp_check = forms.CharField(label="Leave this empty", required=False, widget=forms.TextInput(attrs={
        "tabindex": "-1", "autocomplete": "off", "aria-hidden": "true",
    }))

    class Meta:
        model = ContactRequest
        fields = ["name", "email", "business_name", "service", "what_you_sell", "link", "goal", "message"]
        labels = {
            "name": "Your name",
            "email": "Email",
            "business_name": "Business name",
            "service": "What do you need?",
            "what_you_sell": "What do you sell, and to whom?",
            "link": "Instagram, Facebook or website (optional)",
            "goal": "What do you want to achieve? (optional)",
            "message": "Anything else I should know?",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@business.com", "autocomplete": "email"}),
            "business_name": forms.TextInput(attrs={"placeholder": "Your business"}),
            "what_you_sell": forms.Textarea(attrs={
                "rows": 3, "placeholder": "Short description of your business and your customers"}),
            "link": forms.TextInput(attrs={"placeholder": "Link to your Instagram, Facebook or website"}),
            "goal": forms.TextInput(attrs={"placeholder": "Your main goal"}),
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "For example: a date, a question, a style you like"}),
        }
        error_messages = {
            "name": {"required": "Please enter your name."},
            "email": {"required": "Please enter your email.", "invalid": "Please enter a valid email address."},
            "business_name": {"required": "Please enter your business name."},
            "service": {"required": "Please choose what you need.", "invalid_choice": "Please choose one of the options."},
            "what_you_sell": {"required": "Please tell me what you sell, and to whom."},
        }
        help_texts = {
            "goal": "For example: more messages, more sales, a fully booked event.",
            "link": "One link is enough.",
        }

    def error_fields(self):
        """(label, field id) for each visible field with a problem, for the summary at the top of the form."""
        return [(field.label, field.id_for_label) for field in self if field.errors and field.name != "hp_check"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("hp_check"):
            # Visible message, so a real person whose browser filled the hidden field is not left guessing.
            raise forms.ValidationError("Your request could not be sent. Please reload the page and try again.")
        return cleaned

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        recent = timezone.now() - timedelta(minutes=2)
        if ContactRequest.objects.filter(email__iexact=email, created_at__gte=recent).exists():
            raise forms.ValidationError("I already received your request a moment ago, so there is no need to send it again.")
        return email
