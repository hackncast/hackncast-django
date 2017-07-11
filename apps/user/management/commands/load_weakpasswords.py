from urllib import error, request

from django.core.management.base import BaseCommand
from django.db import connection

from apps.user.models import WeakPassword


class Command(BaseCommand):
    help = "Initialize WekaPassword model"

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', default=None, type=str)

    def handle(self, *args, **options):
        url = options['url']
        if url is None:
            self.stdout.write(
                self.style.ERROR('A URL for fetch the file must be informed:'),
                ending=' '
            )
            self.stdout.write(
                "The content of the URL must be a file with a list of "
                "passwords in each line"
            )
            exit(1)

        try:
            fd = request.urlopen(url)
        except error.HTTPError:
            self.stdout.write(
                self.style.ERROR('The informed URL is invalid!'),
            )

        passwords = [
            WeakPassword(password=password.strip())
            for password in fd.readlines()
        ]

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE user_weakpassword")

        WeakPassword.objects.bulk_create(passwords)
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully loaded {} weak passwords in database'.format(
                    len(passwords)
                )
            ),
        )
