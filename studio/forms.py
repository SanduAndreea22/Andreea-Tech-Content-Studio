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
            "goal": "What do you want to achieve?",
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
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Anything else you want me to know"}),
        }
        help_texts = {
            "goal": "For example: more messages, more sales, a full event.",
            "link": "One link is enough.",
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("hp_check"):
            # Visible message, so a real person whose browser filled the hidden field is not left guessing.
            raise forms.ValidationError("We could not send your request. Please reload the page and try again.")
        return cleaned

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        recent = timezone.now() - timedelta(minutes=2)
        if ContactRequest.objects.filter(email__iexact=email, created_at__gte=recent).exists():
            raise forms.ValidationError("We already got your request. Please wait a couple of minutes before sending another.")
        return email
