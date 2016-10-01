from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from apps.core.models import (EmailUserManager, Location, Schooling,
                              Profession)
from model_utils import Choices

SEX = Choices(
    ('', 'Escolha uma opção...'),
    ('m', 'Masculino'),
    ('f', 'Feminino'),
)
OCCUPATIONS = Choices(
    (None, 'Escolha uma ocupacao...'),
    (0, 'Estudo'),
    (1, 'Trabalho'),
    (2, 'Estudo e trabalho'),
    (3, 'Desocupado'),
)


class HNCUser(Location, AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Endereço de Email', unique=True, max_length=254,
        db_index=True,
    )
    first_name = models.CharField(
        verbose_name='Nome', max_length=50, blank=False,
    )
    last_name = models.CharField(
        verbose_name='Sobrenome', max_length=50, blank=True,
    )
    birthdate = models.DateField(
        verbose_name='Data de Nascimento', null=True,
    )
    sex = models.CharField(
        verbose_name='Sexo', choices=SEX, max_length=20, blank=True,
    )
    occupation = models.IntegerField(
        verbose_name='Ocupação', choices=OCCUPATIONS, null=True,
    )
    schooling = models.ForeignKey(
        verbose_name='Escolaridade', default=None, null=True, to=Schooling,
    )
    profession = models.ForeignKey(
        verbose_name='Profissão', default=None, null=True, to=Profession,
    )
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    # Links

    USERNAME_FIELD = 'email'
    SEX = SEX
    OCCUPATIONS = OCCUPATIONS
    objects = EmailUserManager()

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
