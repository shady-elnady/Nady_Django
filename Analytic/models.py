from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from djongo.models import ArrayReferenceField
from polymorphic.models import PolymorphicModel

from GraphQL.models import BaseModelName
from Person.models import ReferenceLimitingFactor
from Specimen.models import Sample, Specimen
from Unit.models import Unit

# Create your models here.


class Analytics(BaseModelName): # مركب المراد تحليلها
    # TODO CHEMICAL STRCTURE
    molecular_weight= models.SmallIntegerField(
        blank= True,
        null= True,
        verbose_name= _("Molecular Weight"),
    )
    chemical_structure = models.CharField(
        max_length= 50,
        blank= True,
        null= True,
        verbose_name= _("Chemical Structure"),
    )
    units = models.ManyToManyField(
        Unit,
        through= "AnalyticsUnit",
        # related_name= _("Analytics"),
        verbose_name= _("Units"),
    )
    
    class Meta:  
        verbose_name= _("Analytics")
        verbose_name_plural= _("Analytics")



class AnalyticsUnit(models.Model):
    analytics= models.ForeignKey(
        Analytics,
        on_delete= models.CASCADE,
        verbose_name= _("Analytics"),
    )
    unit= models.ForeignKey(
        Unit,
        on_delete= models.CASCADE,
        # related_name= _("Analytics"),
        verbose_name= _("Unit"),
    )
    # convert_to_units= models.ManyToManyField(
    #     "self",
    #     through= _("AnalyticsUnitConvert"),
    #     verbose_name= _("Convert to Units"),
    # )
    is_default= models.BooleanField(
        default= True,
        verbose_name= _("Is Default"),
    )   

    class Meta:
        unique_together= [
            ["analytics", "unit"],
        ]
        verbose_name= _("Analytics Unit")
        verbose_name_plural= _("Analytics Units")


class AnalyticsUnitConvert(models.Model):
    analytics_unit= models.ForeignKey(
        AnalyticsUnit,
        on_delete= models.CASCADE,
        verbose_name= _("Analytics"),
    )
    to_analytics_unit= models.ForeignKey(
        AnalyticsUnit,
        on_delete= models.CASCADE,
        related_name= _("Convert_To_Units"),
        verbose_name= _("Unit"),
    )
    factor= models.BooleanField(
        verbose_name= _("Factor"),
    )   

    class Meta:
        unique_together= [
            [
                "analytics_unit",
                "to_analytics_unit",
            ],
        ]
        verbose_name= _("Analytics Unit Convert")
        verbose_name_plural= _("Analytics Unit Converts")



class ReferenceRange(BaseModelName):
    analytics= models.ForeignKey(
        Analytics,
        on_delete= models.CASCADE,
        related_name= _("Reference_Ranges"), 
        verbose_name= _("Analytics"),
    )
    sample= models.ForeignKey(
        Sample,
        on_delete= models.CASCADE,
        related_name= _("Reference_Ranges"), 
        verbose_name= _("Sample"),
    )
    unit= models.ForeignKey(
        Unit,
        null= True,
        blank= True,
        on_delete= models.CASCADE,
        related_name= _("Reference_Ranges"), 
        verbose_name= _("Unit"),
    )
    lowest_value = models.FloatField(
        null= True,
        blank= True,
        verbose_name= _("Lowest Value"),
    )
    highest_value = models.FloatField(
        null= True,
        blank= True,
        verbose_name= _("Highest Value"), 
    )
    # TODO Many To Many Field Convert To >>>>>>>>>  
    # reference_range_expected_values= models.ManyToManyField(
    #     ReferenceLimitingFactor,
    #     through= "ReferenceRangeExpectedValue",
    #     verbose_name= _("Reference Range Expected Values"),
    # )
    reference_range_expected_values= ArrayReferenceField(
        to="ReferenceRangeExpectedValue",
        on_delete=models.CASCADE,
        verbose_name= _("Reference Range Expected Values"),
    )

    class Meta:
        verbose_name= _("Reference Range")
        verbose_name_plural= _("Reference Ranges")


class ReferenceRangeExpectedValue(models.Model):
    reference_range= models.ForeignKey(
        ReferenceRange,
        on_delete= models.CASCADE,
        related_name= _("reference_range_expected_values+"), 
        verbose_name= _("ReferenceRange"),
    )
    reference_limiting_factors = models.ManyToManyField(
        ReferenceLimitingFactor,
        # related_name= _("+"),
        verbose_name= _("Reference Limiting Factors"),
    ) # Conditions شروط او متطلبات
    min_normal = models.FloatField(
        null= True,
        blank= True,
        verbose_name= _("Minimum Normal"),
    )
    max_normal = models.FloatField(
        null= True,
        blank= True,
        verbose_name= _("Maximum Normal"),
    )

    class Meta:
        verbose_name= _("Reference Range Expected Value")
        verbose_name_plural= _("Reference Range Expected Values")