from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from GraphQL.models import BaseModelName, upload_to
from Facility.models import Departement
from Compound.models import Analytics, ReferenceRange
from Product.models import Product
from Specimen.models import Sample
from Unit.models import Unit

# Create your models here.


class AnalyticalTechnique(BaseModelName):
    departement= models.ForeignKey(
        Departement,
        on_delete= models.CASCADE,
        related_name= _("Analytical_Techniques"),    # TODO Add to ShortCut Mpdel
        verbose_name= _("Departement"),
    )

    class Meta:
        verbose_name= _("Technique Method")
        verbose_name_plural= _("Technique Methods")


class Analyzer(Product):

    class Analyzers(models.TextChoices):
        HematolgyAnalyzer = "HematolgyAnalyzer"
        ElectrolyteAnalyzer = "ElectrolyteAnalyzer"
        UrineAnalyzer = "UrineAnalyzer"
        ChemistryAnalyzer = "ChemistryAnalyzer"

    analyzer_type= models.CharField(
        max_length= 20,
        choices= Analyzers.choices,
        verbose_name= _("Analyzer Type"),
    )
    brochu_url= models.FileField(
        upload_to= upload_to,
        null= True,
        blank= True,
        verbose_name= _("Brouchu URL"),
    )
    test_volume = models.FloatField(
        default= 400,
        verbose_name= _("Test Volume"),   
    )
    is_closed_system = models.BooleanField(
        default= False,
        verbose_name= _("is Closed System"),   
    )
    analytical_technique = models.ManyToManyField(
        AnalyticalTechnique,        
        related_name= _("Analyzers"),
        verbose_name= _("Analytical Technique"),
    )

    class Meta:
        verbose_name= _("Analyzer")
        verbose_name_plural= _("Analyzers")


##############################################################################

# class QualitativeKat(Kat):

#     class Meta:
#         verbose_name= _("Qualitative Kat")
#         verbose_name_plural= _("Qualitative Kats")


# class QuantitativeKat(Kat):
#     normal_range = models.ForeignKey(
#         ENeedNormal,
#         on_delete= models.CASCADE,
#         related_name="%(app_label)s_%(class)s_Normal_range",
#         verbose_name=_("Normal range"),
#     )
#     low_sensitivity= models.FloatField(
#         blank= True,
#         null= True,
#         verbose_name= _("Low Sensitivity"),
#     )
#     high_sensitivity= models.FloatField(
#         blank= True,
#         null= True,
#         verbose_name= _("High Sensitivity"),
#     )
#     unit = models.ForeignKey(
#         Unit,
#         on_delete= models.CASCADE,
#         related_name= "%(app_label)s_%(class)s_Unit",
#         verbose_name= _("Unit"),
#     )

#     class Meta:
#         verbose_name = _("Quantitative Kat")
#         verbose_name_plural = _("Quantitative Kats")


# class OpenSystemKat(QuantitativeKat):

#     class Meta:
#         verbose_name= _("Open System Kat")
#         verbose_name_plural= _("Open System Kats")


class LabSupply(Product): # مستلزمات المعامل

    class Meta:
        verbose_name= _("Laboratory Supply")
        verbose_name_plural= _("Laboratory Supplies")


# NOTE Bind with Medicin
class AntiBioticDisk(LabSupply):
    symbol= models.CharField(
        max_length= 10,
        unique= True,
        verbose_name= _("Symbol"),
    )
    for_child_pregnant= models.BooleanField(
        default= True,
        verbose_name= _("for Child /    gna   nt"),
    )
    anti_biotic= models.ForeignKey(
        Product,
        on_delete= models.CASCADE,
        related_name= _("Anti_Biotic_Disks"),
        verbose_name= _("Anti-Biotic"),
    )

    class Meta:
        verbose_name= _("Anti-Biotic Disk")
        verbose_name_plural= _("Anti-Biotic Disks")



class Standard(LabSupply):
    analytics= models.ForeignKey(
        Analytics,
        on_delete= models.CASCADE,
        related_name= _("Standards"),
        verbose_name= _("Analytics"),
    )
    concentration= models.FloatField(
        verbose_name= _("Concentration"),
    )
    unit= models.ForeignKey(
        Unit,
        on_delete= models.CASCADE,
        related_name= _("Standards"),
        verbose_name= _("Unit"),
    )

    class Meta:
        verbose_name= _("Standard")
        verbose_name_plural= _("Standards")



class Kat(LabSupply):
    analytics= models.ForeignKey(
       Analytics,
        on_delete= models.CASCADE,
        related_name= _("Kats"),
        verbose_name= _("Analytics"),
    )
    analytical_technique= models.ForeignKey(
        AnalyticalTechnique,
        on_delete= models.CASCADE,
        related_name= _("Kats"),
        verbose_name= _("Analytical Technique"),
    )
    samples= models.ManyToManyField(
        Sample,
        through= "KatSample",
        verbose_name= _("Samples"),
    )
    analyzers= models.ManyToManyField(
        Analyzer,
        through= "AnalyzerKat",
        verbose_name= _("Analyzers"),
    )
    low_sensitivity = models.FloatField(
        null= True,
        blank= True,
        verbose_name= _("Low Sensitivity"),
    )
    high_sensitivity = models.FloatField(
        null= True,
        blank= True,
        verbose_name= _("High Sensitivity"),
    )

    class Meta:
        verbose_name= _("Kat")
        verbose_name_plural= _("Kats")


class KatSample(models.Model):
    kat= models.ForeignKey(
        Kat,
        on_delete= models.CASCADE,
        verbose_name= _("Kat"),
    )
    sample= models.ForeignKey(
        Sample,
        on_delete= models.CASCADE,
        related_name= _("Kats"),
        verbose_name= _("Specimen"),
    )
    reference_range= models.ForeignKey(
        ReferenceRange,
        on_delete= models.CASCADE,
        blank= True,
        null= True,
        related_name= _("Kat_Samples"),
        verbose_name= _("Reference Range"),
    )

    @property
    def slug(self):
        return slugify(f"{self.sample.name} {self.kat.name}")

    def __str__(self) -> str:
        return f"{self.sample.name} {self.kat.name}"

    def __decode__(self):
        return f"{self.sample.name} {self.kat.name}"
    
    class Meta:
        unique_together= [
            ["kat", "sample"],
        ]
        verbose_name= _("Kat Sample")
        verbose_name_plural= _("Kat Samples")


class AnalyzerKat(models.Model):
    analyzer= models.ForeignKey(
        Analyzer,
        on_delete= models.CASCADE,
        # related_name= _("Kats"),
        verbose_name= _("Analyzer"),
    )
    kat = models.ForeignKey(
        Kat,
        on_delete= models.CASCADE,
        # related_name= _("Analyzers"),
        verbose_name= _("Analyzer"),
    )
    start_up_consumption= models.FloatField(
        blank= True,
        null= True,
        verbose_name=_("Start Up Consumption"),
    ) # استهلاك الكيماويات فى فتح الجهاز
    test_consumption= models.FloatField(
        blank= True,
        null= True,
        verbose_name= _("Test Consumption"),
    ) # استهلاك الكيماويات لتحليل
    end_consumption= models.FloatField(
        blank= True,
        null= True,
        verbose_name= _("End Consumption"),
    ) # استهلاك الكيماويات فى غلق الجهاز

    class Meta:
        unique_together= [
            ["analyzer", "kat"],
        ]
        verbose_name= _("Analyzer Kat")
        verbose_name_plural= _("Analyzer Kats")

