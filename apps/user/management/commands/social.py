from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = "Configura Social Apps no Django-Allauth"

    def handle(self, *args, **options):

        site = Site.objects.get(id=1)
        site.domain = settings.DJANGO_DOMAIN
        site.name = "Hack 'n' Cast"
        site.save()

        self.add_or_update_app(
            'twitter',
            'twitter',
            settings.TWITTER_SECRET,
            settings.TWITTER_KEY,
            sites=[site]
        )

        self.add_or_update_app(
            'github',
            'github',
            settings.GITHUB_SECRET,
            settings.GITHUB_KEY,
            sites=[site]
        )

        self.add_or_update_app(
            'google',
            'google',
            settings.GOOGLE_SECRET,
            settings.GOOGLE_KEY,
            sites=[site]
        )

    def add_or_update_app(self, provider, name, secret, client_id, sites):
        if not SocialApp.objects.filter(provider=provider).all():
            SocialApp.objects.create(
                provider=provider,
                name=name,
            )
        social = SocialApp.objects.get(provider=provider)
        social.name = name
        social.secret = secret
        social.client_id = client_id
        social.sites = sites
        social.save()
        self.stdout.write(
            self.style.SUCCESS("{} atualizado com sucesso".format(name))
        )
