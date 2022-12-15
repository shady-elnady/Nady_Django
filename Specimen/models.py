from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from GraphQL.models import BaseModelName
from Person.models import ReferenceLimitingFactor

# Create your models here.


class Sample(BaseModelName):
    
    class Meta:
        verbose_name= _("Sample")
        verbose_name_plural= _("Samples")


class SamplingContainer(ReferenceLimitingFactor):
    
    class Meta:
        verbose_name= _("Sampling Container")
        verbose_name_plural= _("Sampling Containers")


class SamplingTime(ReferenceLimitingFactor): 
    time = models.TimeField(
        verbose_name= _("Time"),
    )
    
    class Meta:
        verbose_name= _("Sampling Time")
        verbose_name_plural= _("Sampling Times")


class Specimen(BaseModelName):
    sample = models.ForeignKey(
        Sample,
        on_delete= models.CASCADE,
        related_name= _("Specimens"),    # TODO Add to Sample Mpdel
        verbose_name= _("Sample"),
    )
    reference_limiting_factors = models.ManyToManyField(
        ReferenceLimitingFactor,
        related_name= _("+"),
        verbose_name= _("Reference Limiting Factors"),
    ) # Conditions شروط او متطلبات
    comment = models.TextField(
        max_length= 200,
        blank= True,
        null= True,
        verbose_name= _("Comment"),
    )

    class Meta:
        verbose_name = _("Specimen")
        verbose_name_plural = _("Specimens")

