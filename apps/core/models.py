from django.db import models
from apps.core.querysets import BaseModelQuerySet
from django.utils.translation import ugettext as _
from django.contrib.auth.base_user import BaseUserManager
from cities_light.abstract_models import (
    AbstractRegion, AbstractCountry, AbstractCity
)
from cities_light.receivers import connect_default_signals


class EmailUserManager(BaseUserManager):
    def create_user(self, *args, **kwargs):
        """
        Cria e salva um usuario com os dados passados via kwargs.
        """

        email = kwargs["email"]
        email = self.normalize_email(email)
        password = kwargs["password"]
        kwargs.pop("password")

        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(**kwargs)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, *args, **kwargs):
        """
        Cria e salva um superusuario com os dados passados via kwargs.
        """

        user = self.create_user(**kwargs)
        user.is_admin = True
        user.save(using=self._db)
        return user


class BaseModel(models.Model):
    """ Model base do sistema """

    is_active = models.BooleanField(_('Ativo'), default=True)
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Modificado em'), auto_now=True)
    media_path = ''

    objects = BaseModelQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ('-updated_at',)


class Country(AbstractCountry):
    name_pt = models.CharField(max_length=200, null=True, db_index=True)

    def __str__(self):
        alternate_name = self.alternate_names.split(';')[0]
        return alternate_name if alternate_name else self.name

    class Meta:
        verbose_name = _("País")
        verbose_name_plural = _("Países")
        ordering = ['alternate_names']

connect_default_signals(Country)


class Region(AbstractRegion):
    name_pt = models.CharField(max_length=200, null=True, db_index=True)

    def __str__(self):
        alternate_name = self.alternate_names.split(';')[0]
        return alternate_name if alternate_name else self.name

    class Meta:
        verbose_name = _("Estado")
        verbose_name_plural = _("Estados")
        ordering = ['alternate_names']

connect_default_signals(Region)


class City(AbstractCity):
    name_pt = models.CharField(max_length=200, null=True, db_index=True)

    def __str__(self):
        alternate_name = self.alternate_names.split(';')[0]
        return alternate_name if alternate_name else self.name

    class Meta:
        verbose_name = _("Cidade")
        verbose_name_plural = _("Cidades")
        ordering = ['alternate_names']

connect_default_signals(City)


class Location(models.Model):
    country = models.ForeignKey(
        verbose_name=_("País"),
        null=True,
        to=Country,
    )
    region = models.ForeignKey(
        verbose_name=_("Estado"),
        null=True,
        to=Region,
    )
    city = models.ForeignKey(
        verbose_name=_("Cidade"),
        null=True,
        to=City,
    )

    class Meta:
        abstract = True


class Schooling(models.Model):
    level = models.CharField(
        max_length=150, verbose_name='Nivel', db_index=True
    )

    def __str__(self):
        return self.level


class Profession(models.Model):
    name = models.CharField(
        max_length=150, verbose_name='Nome', db_index=True
    )

    def __str__(self):
        return self.name
