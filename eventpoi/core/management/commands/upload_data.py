from django.core.management.base import NoArgsCommand
from core.tools.tests import upload_data


class Command(NoArgsCommand):
    help = "Upload test data"

    def handle_noargs(self, **options):
        upload_data()