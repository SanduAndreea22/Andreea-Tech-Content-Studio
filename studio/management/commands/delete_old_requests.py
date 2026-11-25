from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from studio.models import ContactRequest


class Command(BaseCommand):
    help = (
        "Delete form messages older than N months (default 12), as the Privacy page promises. "
        "Without --yes it only shows how many would be deleted."
    )

    def add_arguments(self, parser):
        parser.add_argument("--months", type=int, default=12)
        parser.add_argument("--yes", action="store_true", help="Really delete.")

    def handle(self, *args, **options):
        months = options["months"]
        cutoff = timezone.now() - timedelta(days=months * 30.44)
        old = ContactRequest.objects.filter(created_at__lt=cutoff)
        count = old.count()
        if not options["yes"]:
            self.stdout.write(f"{count} message(s) older than {months} months. Run again with --yes to delete them.")
            return
        old.delete()
        self.stdout.write(f"Deleted {count} message(s) older than {months} months.")
