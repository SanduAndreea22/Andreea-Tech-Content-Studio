import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactRequest, SampleProject, validate_pdf

PDF_BYTES = b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF"
TEMP_MEDIA = tempfile.mkdtemp()


def valid_post(**overrides):
    data = {
        "name": "Test Person",
        "email": "test@example.com",
        "business_name": "Test Bakery",
        "service": "ads",
        "what_you_sell": "Bread, to people in the neighbourhood.",
        "link": "",
        "goal": "More orders",
        "message": "",
        "hp_check": "",
    }
    data.update(overrides)
    return data


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class SiteTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)

    def make_sample(self, **kwargs):
        defaults = dict(
            title="Sample ad", category="ad", description="An example.",
            pdf=SimpleUploadedFile("a.pdf", PDF_BYTES, content_type="application/pdf"),
        )
        defaults.update(kwargs)
        return SampleProject.objects.create(**defaults)

    def test_public_pages_load(self):
        for name in ["home", "services", "packages", "portfolio", "about", "contact", "contact_thanks"]:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_footer_shows_contact_links_and_hides_empty_ones(self):
        html = self.client.get(reverse("home")).content.decode()
        self.assertIn("linkedin.com/in/andreeasandu22", html)
        self.assertIn("mailto:andreea.sandu.copy@gmail.com", html)
        self.assertNotIn("Instagram</a>", html)
        self.assertNotIn("Facebook</a>", html)

    def test_packages_show_prices(self):
        html = self.client.get(reverse("packages")).content.decode()
        for price in ["€30", "€75", "€45", "€110", "€200"]:
            self.assertIn(price, html)

    def test_contact_saves_request(self):
        response = self.client.post(reverse("contact"), valid_post())
        self.assertRedirects(response, reverse("contact_thanks"))
        saved = ContactRequest.objects.get()
        self.assertEqual(saved.status, "new")
        self.assertEqual(saved.business_name, "Test Bakery")

    def test_contact_requires_fields(self):
        response = self.client.post(reverse("contact"), valid_post(name="", email="not-an-email"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactRequest.objects.count(), 0)

    def test_honeypot_blocks_bots(self):
        response = self.client.post(reverse("contact"), valid_post(hp_check="http://spam.example"))
        self.assertEqual(ContactRequest.objects.count(), 0)
        self.assertContains(response, "Please reload the page and try again")

    def test_uploaded_pdf_gets_random_name(self):
        sample = self.make_sample(pdf=SimpleUploadedFile("my-secret-draft.pdf", PDF_BYTES))
        self.assertNotIn("my-secret-draft", sample.pdf.name)
        self.assertRegex(sample.pdf.name, r"^samples/[0-9a-f]{32}\.pdf$")

    def test_portfolio_detail_shows_pdf(self):
        sample = self.make_sample()
        response = self.client.get(reverse("portfolio_detail", args=[sample.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, sample.pdf.url)

    def test_same_email_twice_quickly_is_blocked(self):
        self.client.post(reverse("contact"), valid_post())
        self.client.post(reverse("contact"), valid_post())
        self.assertEqual(ContactRequest.objects.count(), 1)

    def test_service_prefill_ignores_unknown_values(self):
        response = self.client.get(reverse("contact") + "?service=zzinject")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("zzinject", response.content.decode())
        self.assertContains(response, '<option value="unsure" selected>')

    def test_portfolio_hides_unpublished(self):
        self.make_sample(title="Visible")
        self.make_sample(title="Hidden", is_published=False,
                         pdf=SimpleUploadedFile("b.pdf", PDF_BYTES, content_type="application/pdf"))
        html = self.client.get(reverse("portfolio")).content.decode()
        self.assertIn("Visible", html)
        self.assertNotIn("Hidden", html)

    def test_unpublished_detail_is_404(self):
        sample = self.make_sample(is_published=False)
        self.assertEqual(self.client.get(reverse("portfolio_detail", args=[sample.pk])).status_code, 404)

    def test_portfolio_filter_by_category(self):
        self.make_sample(title="An ad", category="ad")
        self.make_sample(title="Some posts", category="posts",
                         pdf=SimpleUploadedFile("c.pdf", PDF_BYTES, content_type="application/pdf"))
        html = self.client.get(reverse("portfolio") + "?category=posts").content.decode()
        self.assertIn("Some posts", html)
        self.assertNotIn("An ad", html)

    def test_pdf_validator_rejects_fake_pdf(self):
        fake = SimpleUploadedFile("evil.pdf", b"<html>not a pdf</html>")
        with self.assertRaises(ValidationError):
            validate_pdf(fake)

    def test_pdf_validator_accepts_real_pdf(self):
        validate_pdf(SimpleUploadedFile("ok.pdf", PDF_BYTES))

    def test_admin_requires_login(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_admin_lists_messages(self):
        ContactRequest.objects.create(name="A", email="a@example.com", business_name="B", what_you_sell="x", goal="y")
        user = get_user_model().objects.create_superuser("andreea", "a@example.com", "a-long-test-password-1")
        self.client.force_login(user)
        response = self.client.get("/admin/studio/contactrequest/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "B (A)")
