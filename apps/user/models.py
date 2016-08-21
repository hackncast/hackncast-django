from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

from apps.core.querysets import BaseModelQuerySet


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


class HNCUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Endereço de Email',
        unique=True,
        max_length=254,
    )
    first_name = models.CharField(
        verbose_name='Nome',
        max_length=50,
        blank=False,
        help_text='Informe o nome',
    )
    last_name = models.CharField(
        verbose_name='Sobrenome',
        max_length=50,
        blank=False,
        help_text='Informe o sobrenome',
    )
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    objects = EmailUserManager()
