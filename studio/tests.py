import shutil
import tempfile

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.utils import timezone
import io
from io import StringIO

from PIL import Image
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
        for name in ["home", "services", "packages", "portfolio", "about", "contact", "free_sample", "free_sample_thanks"]:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_footer_shows_contact_links_and_hides_empty_ones(self):
        html = self.client.get(reverse("home")).content.decode()
        self.assertIn("linkedin.com/in/andreeasandu22", html)
        self.assertIn("mailto:andreea.sandu.copy@gmail.com", html)
        self.assertNotIn("Instagram</a>", html)
        self.assertNotIn("Facebook</a>", html)

    def test_contact_page_has_no_form_and_links_to_free_sample(self):
        response = self.client.get(reverse("contact"))
        self.assertNotContains(response, "<form")
        self.assertContains(response, reverse("free_sample"))
        self.assertContains(response, "mailto:andreea.sandu.copy@gmail.com")

    def test_every_get_your_free_sample_button_goes_to_the_form(self):
        for name in ["home", "services", "about", "packages"]:
            with self.subTest(page=name):
                html = self.client.get(reverse(name)).content.decode()
                self.assertIn('href="%s">Get your free ad' % reverse("free_sample"), html)

    def test_home_headline_says_what_is_sold(self):
        html = self.client.get(reverse("home")).content.decode()
        self.assertIn("<h1>Ads and social media posts written for your business.</h1>", html)
        self.assertIn("So your customers understand what you offer and what to do next.", html)
        self.assertIn("Three ways I can help", html)

    def test_problem_first_ads_are_not_a_separate_service(self):
        for name in ["home", "services", "about"]:
            with self.subTest(page=name):
                html = self.client.get(reverse(name)).content.decode()
                self.assertNotIn("Ads built on your customer", html)
                self.assertIn("starts from a problem your customer feels", html)

    def test_one_name_per_service(self):
        for name in ["home", "services", "about"]:
            with self.subTest(page=name):
                html = self.client.get(reverse(name)).content.decode()
                self.assertNotIn("Advertising copy", html)
                self.assertNotIn("Promotional content", html)
                self.assertNotIn("Marketing &amp; promotional", html)
                self.assertIn("Product, service &amp; event texts", html)

    def test_two_working_days_is_stated(self):
        for name in ["home", "free_sample", "free_sample_thanks"]:
            with self.subTest(page=name):
                self.assertContains(self.client.get(reverse(name)), "within 2 working days")

    def test_goal_is_optional(self):
        response = self.client.post(reverse("free_sample"), valid_post(goal=""))
        self.assertRedirects(response, reverse("free_sample_thanks"))
        self.assertEqual(ContactRequest.objects.get().goal, "")

    def test_services_explains_how_we_work(self):
        html = self.client.get(reverse("services")).content.decode()
        self.assertIn('id="how-we-work"', html)
        self.assertIn("You pay upfront. Once you select a package, I'll send you the payment details.", html)
        self.assertIn("Each time takes me up to 2 working days", html)
        self.assertIn("The time counts from the day I receive your payment", html)

    def test_delivery_days_come_from_one_place(self):
        services = self.client.get(reverse("services")).content.decode()
        packages = self.client.get(reverse("packages")).content.decode()
        for name, days in [("1 Ad", 3), ("3 Ads", 3), ("Starter Posts", 3), ("Standard Posts", 5), ("Full Month", 7)]:
            self.assertIn(f"<b>{name}</b> <span>{days} working days</span>", services)
        self.assertIn("Ready in 7 working days", packages)
        self.assertIn("Ready in 5 working days", packages)

    def test_home_links_to_full_process(self):
        self.assertContains(self.client.get(reverse("home")), "/services/#how-we-work")

    def test_hero_has_real_text_and_button(self):
        html = self.client.get(reverse("home")).content.decode()
        hero = html.split('<section class="hero">')[1].split("</section>")[0]
        self.assertIn("<h1>Ads and social media posts written for your business.</h1>", hero)
        self.assertIn("Copywriter &amp; Social Media Content Creator", hero)
        self.assertIn("Andreea Sandu", hero)
        self.assertIn('href="%s">Get your free ad' % reverse("free_sample"), hero)
        self.assertEqual(html.count("<h1"), 1)

    def test_privacy_page_and_links(self):
        response = self.client.get(reverse("privacy"))
        self.assertContains(response, "Up to 12 months after your request")
        self.assertContains(response, "mailto:andreea.sandu.copy@gmail.com")
        self.assertContains(self.client.get(reverse("home")), reverse("privacy"))
        self.assertContains(self.client.get(reverse("free_sample")), reverse("privacy"))

    def test_hero_says_who_it_is_for(self):
        self.assertContains(self.client.get(reverse("home")),
                            "Writing ads and posts takes time. If you're short on time, or don't know where to start, I write them for you.")

    def _request(self, email, age_days):
        r = ContactRequest.objects.create(name="N", email=email, business_name="B", what_you_sell="x")
        ContactRequest.objects.filter(pk=r.pk).update(created_at=timezone.now() - timedelta(days=age_days))
        return r

    def test_delete_old_requests_asks_before_deleting(self):
        self._request("old@example.com", 400)
        self._request("new@example.com", 30)
        out = StringIO()
        call_command("delete_old_requests", stdout=out)
        self.assertEqual(ContactRequest.objects.count(), 2)
        self.assertIn("1 message(s) older than 12 months", out.getvalue())

    def test_delete_old_requests_with_yes_keeps_recent_ones(self):
        self._request("old@example.com", 400)
        keep = self._request("new@example.com", 30)
        call_command("delete_old_requests", "--yes", stdout=StringIO())
        self.assertEqual(list(ContactRequest.objects.values_list("pk", flat=True)), [keep.pk])

    def test_no_jargon_and_one_word_per_idea(self):
        banned = ["button to act", "call to action", "calls to action", "No hourly billing", "messages that sell",
                  "sales-focused", "target audience", "brand preferences", "post concepts", "post ideas", "carousel content"]
        for name in ["home", "services", "packages", "about", "free_sample", "contact", "free_sample_thanks"]:
            html = self.client.get(reverse(name)).content.decode()
            for phrase in banned:
                with self.subTest(page=name, phrase=phrase):
                    self.assertNotIn(phrase, html)

    def test_every_ad_package_starts_from_the_customers_problem(self):
        html = self.client.get(reverse("packages")).content.decode()
        self.assertEqual(html.count("starts from your customer&#x27;s problem") + html.count("Starts from your customer&#x27;s problem"), 2)

    def test_packages_say_the_time_counts_after_payment(self):
        self.assertContains(self.client.get(reverse("packages")), "working days after payment")

    def test_one_name_for_the_offer(self):
        for name in ["home", "services", "packages", "about", "contact", "free_sample", "free_sample_thanks"]:
            html = self.client.get(reverse(name)).content.decode()
            with self.subTest(page=name):
                self.assertNotIn("free sample", html.lower().replace("free-sample", "").replace("free_sample", "").replace("sample project", ""))

    def test_text_price_is_shown_once_in_one_place(self):
        self.assertContains(self.client.get(reverse("packages")), "They cost €15 per text, a fixed price.")
        self.assertContains(self.client.get(reverse("services")), "Fixed price: €15 per text.")

    def test_carousels_are_counted_inside_the_posts(self):
        html = self.client.get(reverse("packages")).content.decode()
        self.assertIn("8 posts, including 1 carousel", html)
        self.assertIn("12 posts, including 2 carousels", html)
        self.assertNotIn("Growth Pack", html)

    def test_contact_states_reply_time(self):
        self.assertContains(self.client.get(reverse("contact")), "I reply within 2 working days")

    def test_social_preview_tags_use_an_absolute_image(self):
        html = self.client.get(reverse("home")).content.decode()
        self.assertIn('property="og:image" content="http://testserver/static/studio/img/og-image.jpg"', html)
        self.assertIn('property="og:title"', html)
        self.assertIn('name="twitter:card" content="summary_large_image"', html)

    def test_sticky_button_is_on_content_pages_but_not_on_the_form_pages(self):
        for name in ["home", "services", "packages", "portfolio", "about", "contact", "privacy"]:
            with self.subTest(page=name):
                self.assertContains(self.client.get(reverse(name)), 'id="sticky-cta"')
        for name in ["free_sample", "free_sample_thanks"]:
            with self.subTest(page=name):
                self.assertNotContains(self.client.get(reverse(name)), 'id="sticky-cta"')

    def test_faq_answers_use_the_real_rules(self):
        html = self.client.get(reverse("services")).content.decode()
        self.assertEqual(html.count("<details>"), 8)
        self.assertIn("From 3 to 7 working days", html)
        self.assertIn("from €30 for ads and from €45 for posts", html)
        self.assertIn("€15 per text", html)

    def test_how_we_work_is_the_cream_band(self):
        self.assertContains(self.client.get(reverse("services")), '<section class="pad cream" id="how-we-work">')

    def test_sample_card_shows_cover_picture_or_pdf_label(self):
        buf = io.BytesIO(); Image.new("RGB", (8, 8), (212, 165, 90)).save(buf, "PNG")
        self.make_sample(title="With cover", cover=SimpleUploadedFile("c.png", buf.getvalue(), content_type="image/png"))
        self.make_sample(title="Without cover", pdf=SimpleUploadedFile("n.pdf", PDF_BYTES, content_type="application/pdf"))
        html = self.client.get(reverse("portfolio")).content.decode()
        self.assertRegex(html, r'<img src="/media/samples/covers/[0-9a-f]{32}\.png"')
        self.assertEqual(html.count('<span class="pdf">PDF</span>'), 1)

    def test_cover_must_be_a_real_picture_type(self):
        sample = self.make_sample()
        sample.cover = SimpleUploadedFile("x.svg", b"<svg xmlns='http://www.w3.org/2000/svg'/>", content_type="image/svg+xml")
        with self.assertRaises(ValidationError):
            sample.full_clean()

    def test_thank_you_page_shows_what_happens_next(self):
        html = self.client.get(reverse("free_sample_thanks")).content.decode()
        self.assertIn('class="ring-draw"', html)
        steps = html.split('<ol class="next-steps">')[1].split("</ol>")[0]
        self.assertEqual(steps.count("<li>"), 3)
        self.assertIn("I send you one free ad by email within 2 working days.", html)

    def test_form_page_has_small_photo_for_phones(self):
        html = self.client.get(reverse("free_sample")).content.decode()
        self.assertIn('class="form-avatar"', html)
        self.assertIn('class="side-card form-aside"', html)

    def test_empty_form_says_exactly_what_is_missing(self):
        html = self.client.post(reverse("free_sample"), {}).content.decode()
        for message in ["Please enter your name.", "Please enter your email.", "Please enter your business name.",
                        "Please tell me what you sell, and to whom."]:
            with self.subTest(message=message):
                self.assertIn(message, html)
        self.assertNotIn("This field is required", html)

    def test_failed_send_shows_a_summary_with_links_to_the_fields(self):
        html = self.client.post(reverse("free_sample"), {}).content.decode()
        self.assertIn('id="form-errors"', html)
        self.assertIn("Please check the fields marked below:", html)
        for field_id in ["id_name", "id_email", "id_business_name", "id_what_you_sell"]:
            self.assertIn('href="#%s"' % field_id, html)

    def test_no_summary_on_a_fresh_form(self):
        html = self.client.get(reverse("free_sample")).content.decode()
        self.assertNotIn('id="form-errors"', html)

    def test_bad_email_has_a_plain_message(self):
        html = self.client.post(reverse("free_sample"), valid_post(email="abc")).content.decode()
        self.assertIn("Please enter a valid email address.", html)
        self.assertIn('href="#id_email"', html)

    def test_thank_you_page_says_where_the_email_comes_from(self):
        html = self.client.get(reverse("free_sample_thanks")).content.decode()
        self.assertIn("I'll write to you from andreea.sandu.copy@gmail.com.", html)
        self.assertIn("check your spam folder", html)

    def test_required_fields_are_marked(self):
        html = self.client.get(reverse("free_sample")).content.decode()
        self.assertEqual(html.count('class="field req"') + html.count('class="field full req"'), 4)

    def test_package_note_shows_at_the_top_when_a_package_was_chosen(self):
        html = self.client.get(reverse("free_sample") + "?package=Standard%20Posts").content.decode()
        self.assertIn("You asked about <b>Standard Posts</b> (€110). You still get your free ad first.", html)
        self.assertNotIn("package-note", self.client.get(reverse("free_sample")).content.decode().split("<form")[0].replace(".package-note", ""))

    def test_package_note_stays_when_the_form_comes_back_with_errors(self):
        html = self.client.post(reverse("free_sample") + "?package=Full%20Month", {}).content.decode()
        self.assertIn("You asked about <b>Full Month</b>", html)

    def test_unknown_package_shows_no_note(self):
        self.assertNotContains(self.client.get(reverse("free_sample") + "?package=zzinject"), "You asked about")

    def test_extra_fields_are_folded_away_until_needed(self):
        fresh = self.client.get(reverse("free_sample")).content.decode()
        self.assertIn('<details class="more-details" >', fresh)
        self.assertIn("Add more details (optional)", fresh)
        chosen = self.client.get(reverse("free_sample") + "?package=Full%20Month").content.decode()
        self.assertIn('<details class="more-details" open>', chosen)
        too_long = self.client.post(reverse("free_sample"), valid_post(message="x" * 2001)).content.decode()
        self.assertIn('<details class="more-details" open>', too_long)

    def test_goal_stays_visible_outside_the_folded_part(self):
        html = self.client.get(reverse("free_sample")).content.decode()
        folded = html.split('<details class="more-details"')[1].split("</details>")[0]
        self.assertIn('id="id_link"', folded)
        self.assertIn('id="id_message"', folded)
        self.assertNotIn('id="id_goal"', folded)

    def test_buttons_and_messages_say_what_really_happens(self):
        self.assertContains(self.client.get(reverse("free_sample")), "Send my request")
        self.assertNotContains(self.client.get(reverse("free_sample")), "Send and get my free ad")
        self.client.post(reverse("free_sample"), valid_post())
        again = self.client.post(reverse("free_sample"), valid_post()).content.decode()
        self.assertIn("I already received your request a moment ago, so there is no need to send it again.", again)
        spam = self.client.post(reverse("free_sample"), valid_post(email="other@example.com", hp_check="x")).content.decode()
        self.assertIn("Your request could not be sent. Please reload the page and try again.", spam)

    def test_site_speaks_in_first_person_and_with_contractions(self):
        import re
        for name in ["home", "services", "packages", "free_sample", "free_sample_thanks", "contact", "privacy", "portfolio"]:
            html = self.client.get(reverse(name)).content.decode()
            text = re.sub(r"<[^>]+>", " ", html)
            with self.subTest(page=name):
                self.assertIsNone(re.search(r"\bWe\b", text))
                for stiff in ["do not", "I will ", "does not", "cannot"]:
                    self.assertNotIn(stiff, text)

    def test_privacy_says_what_the_details_are_used_for(self):
        self.assertContains(self.client.get(reverse("privacy")), "to write your free ad and, if you choose a package, your texts.")

    def test_ads_have_an_example_of_the_next_step(self):
        for name in ["home", "services"]:
            with self.subTest(page=name):
                self.assertContains(self.client.get(reverse(name)), "for example: call, send a message or visit your shop.")

    def test_contact_page_texts_are_plain(self):
        html = self.client.get(reverse("contact")).content.decode()
        self.assertIn("For questions, send me an email and I reply within 2 working days.", html)
        self.assertIn("Andreea Sandu on LinkedIn", html)
        self.assertNotIn(">https://www.linkedin.com", html)

    def test_admin_status_uses_the_same_word_as_the_site(self):
        labels = [label for _, label in ContactRequest.STATUS_CHOICES]
        self.assertIn("Ad sent", labels)
        self.assertNotIn("Sample sent", labels)

    def test_contact_page_has_privacy_note(self):
        self.assertContains(self.client.get(reverse("free_sample")), "I use your details only to reply")

    def test_package_button_prefills_message(self):
        response = self.client.get(reverse("free_sample") + "?service=posts&package=Full%20Month")
        self.assertContains(response, "I&#x27;m interested in the Full Month package (€200).")

    def test_unknown_package_is_ignored(self):
        response = self.client.get(reverse("free_sample") + "?package=zzinject")
        self.assertNotContains(response, "zzinject")

    def test_packages_page_links_carry_the_package_name(self):
        html = self.client.get(reverse("packages")).content.decode()
        self.assertIn("package=Full%20Month", html)
        self.assertIn("package=1%20Ad", html)

    def test_empty_portfolio_hides_filters(self):
        html = self.client.get(reverse("portfolio")).content.decode()
        self.assertIn("coming soon", html)
        self.assertNotIn("Open a card", html)
        self.assertNotIn('class="chip', html)

    def test_empty_category_keeps_filters_and_explains(self):
        self.make_sample(category="ad")
        html = self.client.get(reverse("portfolio") + "?category=reels").content.decode()
        self.assertIn("No samples in this category yet", html)
        self.assertIn('class="chip', html)

    def test_services_show_starting_prices(self):
        html = self.client.get(reverse("services")).content.decode()
        self.assertIn("Packages from €30", html)
        self.assertIn("Packages from €45", html)

    def test_packages_show_prices(self):
        html = self.client.get(reverse("packages")).content.decode()
        for price in ["€30", "€75", "€45", "€110", "€200"]:
            self.assertIn(price, html)

    def test_contact_saves_request(self):
        response = self.client.post(reverse("free_sample"), valid_post())
        self.assertRedirects(response, reverse("free_sample_thanks"))
        saved = ContactRequest.objects.get()
        self.assertEqual(saved.status, "new")
        self.assertEqual(saved.business_name, "Test Bakery")

    def test_contact_requires_fields(self):
        response = self.client.post(reverse("free_sample"), valid_post(name="", email="not-an-email"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactRequest.objects.count(), 0)

    def test_honeypot_blocks_bots(self):
        response = self.client.post(reverse("free_sample"), valid_post(hp_check="http://spam.example"))
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
        self.client.post(reverse("free_sample"), valid_post())
        self.client.post(reverse("free_sample"), valid_post())
        self.assertEqual(ContactRequest.objects.count(), 1)

    def test_service_prefill_ignores_unknown_values(self):
        response = self.client.get(reverse("free_sample") + "?service=zzinject")
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
