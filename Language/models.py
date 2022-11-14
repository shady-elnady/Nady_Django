from enum import unique
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from GraphQL.models import BaseModelNative

# Create your models here.


class Language(BaseModelNative):
    iso_639_1 = models.CharField(
        max_length=5,
        unique=True,
        verbose_name = _("ISO_639_1"),
    )
    rtl = models.BooleanField(
        default=False,
        verbose_name=_("RightToLeft"),
    )
    # is_active = models.BooleanField(
    #     default=True,
    #     verbose_name=_("is_Active"),
    # )

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
