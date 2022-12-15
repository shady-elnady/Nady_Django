from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from polymorphic.models import PolymorphicModel
from Facility.models import Departement, Facility

from GraphQL.models import BaseModelImageOnly, BaseModelName, FacilityTypes, Runs, Scores
from Kat.models import AnalyticalTechnique, Kat
from Compound.models import Analytics, ReferenceRange
from Person.models import ReferenceLimitingFactor
from Specimen.models import Sample, Specimen

# Create your models here.


class ShortCut(BaseModelName):
    
    class Meta:
        verbose_name= _("ShortCut")
        verbose_name_plural= _("ShortCuts")


class ShortCutImage(BaseModelImageOnly):
    shortCut= models.ForeignKey(
        ShortCut,
        on_delete= models.CASCADE,
        related_name= _("ShortCut_Images"),    # TODO Add to ShortCut Model
        verbose_name= _("ShortCut"),
    )

    class Meta:
        verbose_name= _("ShortCut Image")
        verbose_name_plural= _("ShortCut Images")


class Analysis(PolymorphicModel, BaseModelName):
    symbol= models.CharField(
        max_length= 10,
        unique= True,
        verbose_name= _("Symbol"),
    )
    shortCuts= models.ManyToManyField(
        ShortCut,
        # related_name= _("+"),
        verbose_name= _("ShortCuts"),
    )
    specimens= models.ManyToManyField(
        Specimen,
        through= "AnalysisSpecimen",
        verbose_name= _("Specimens"),
    )
    analysis_methods= models.ManyToManyField(
        AnalyticalTechnique,
        through= "AnalysisMethod",
        through_fields= ("analysis", "analytical_technique"),
        verbose_name= _("Analysis Methods"),
    )
    is_independent_report= models.BooleanField(
        default= False,
        verbose_name= _("is Independent Report"),
    ) # تقرير مستقل

    class Meta:
        verbose_name= _("Analysis")
        verbose_name_plural= _("Analysis")


class AnalysisSpecimen(models.Model):
    analysis= models.ForeignKey(
        Analysis,
        on_delete= models.CASCADE,
        verbose_name= _("Analysis"),
    )
    specimen= models.ForeignKey(
        Specimen,
        on_delete= models.CASCADE,
        related_name= _("Analysis"),
        verbose_name= _("Specimen"),
    )
    score= models.CharField(
        max_length= 1,
        choices= Scores.choices,
        default= Scores.A,
        verbose_name= _("Score"),
    )
    is_default= models.BooleanField(
        default= True,
        verbose_name= _("Is Default"),
    )

    @property
    def slug(self):
        return slugify(f"{self.specimen.name} {self.analysis.name}")

    def __str__(self) -> str:
        return f"{self.specimen.name} {self.analysis.name}"

    def __decode__(self):
        return f"{self.specimen.name} {self.analysis.name}"
    
    class Meta:
        unique_together= [
            ["analysis", "specimen"],
        ]
        verbose_name= _("Analysis Specimen")
        verbose_name_plural= _("Analysis Specimens")


class Report(Analysis):
    
    class Meta:
        verbose_name= _("Report")
        verbose_name_plural= _("Reports")


class Function(Analysis):

    class Meta:
        verbose_name= _("Function")
        verbose_name_plural= _("Functions")


class GroupAnalysis(Analysis):
    belong_to_function= models.ForeignKey(
        Function,
        on_delete= models.CASCADE,
        null= True,
        blank= True,
        related_name= _("Analysis_in_Function"),
        verbose_name= _("Function"),
    )

    class Meta:
        verbose_name= _("Group Analysis")
        verbose_name_plural= _("Group Analysis")


class Parameter(Analysis):
    analytics = models.ForeignKey(
        Analytics,
        on_delete= models.CASCADE,
        related_name= _("Parameters"),  # TODO add to Analytics Model
        verbose_name= _("Analytics"),
    )
    sample= models.ForeignKey(
        Sample,
        null= True,
        blank= True,
        on_delete= models.CASCADE,
        related_name= _("Parameters"),
        verbose_name= _("Sample"),
    )
    group= models.ForeignKey(
        GroupAnalysis,
        on_delete= models.CASCADE,
        null= True,
        blank= True,
        related_name= _("Parameters_in_Group"),
        verbose_name= _("Group"),
    )
    belong_to_function= models.ForeignKey(
        Function,
        on_delete= models.CASCADE,
        null= True,
        blank= True,
        related_name= _("Parameters_in_Function"),
        verbose_name= _("Function"),
    )
    belong_to_report= models.ForeignKey(
        Report,
        on_delete= models.CASCADE,
        null= True,
        blank= True,
        related_name= _("Parameters_in_Report"),
        verbose_name= _("Report"),
    )
    reference_limiting_factors = models.ManyToManyField(
        ReferenceLimitingFactor,
        related_name= _("+"),
        verbose_name= _("Reference Limiting Factors"),
    ) # Conditions شروط او متطلبات
    sub_analysis= models.ManyToManyField(
        "self",
        verbose_name= _("Sub Analysis"),
    )
    is_constant= models.BooleanField(
        default= False,
        verbose_name= _("is Constant"),
    )

    class Meta:  
        verbose_name= _("Parameter")
        verbose_name_plural= _("Parameters")


class AnalysisMethod(Analysis):
    analysis = models.ForeignKey(
        Analysis,
        on_delete= models.CASCADE,
        related_name= _("Analysis"),
        verbose_name= _("Analysis"),
    )
    analytical_technique = models.ForeignKey(
        AnalyticalTechnique,
        on_delete= models.CASCADE,
        related_name= _("Analysis"),
        verbose_name= _("Analytical Technique"),
    )
    departement = models.ForeignKey(
        Departement,
        on_delete= models.CASCADE,
        null= True,
        blank= True,
        related_name= _("Analysis"),
        verbose_name= _("Departement"),
    )
    price_for_patient= models.FloatField(
        null= True,
        blank= True,
        verbose_name= _("Price For Patient"),  
    )
    price_for_laboratories= models.FloatField(
        null= True,
        blank= True,
        verbose_name= _("Price For Laboratories"),
    )
    score= models.CharField(
        max_length= 1,
        choices= Scores.choices,
        verbose_name= _("Score"),
    )
    is_default= models.BooleanField(
        default= True,
        verbose_name= _("is Default"),
    )

    class Meta:
        verbose_name= _("Analysis Method")
        verbose_name_plural= _("Analysis Methods")


class AnalysisMethodExpectedResult(models.Model):
    analysis_method = models.ForeignKey(
        AnalysisMethod,
        on_delete= models.CASCADE,
        related_name= _("Analysis_Method_Expected_Values"),  # TODO add to AnalysisMethod Model
        verbose_name= _("AnalysisMethod"),
    )
    value= models.CharField(
        max_length= 40,
        verbose_name= _("Value"),
    )
    is_default_value= models.BooleanField(
        default= False,
        verbose_name= _("is Defaul Value"),
    )
    is_Normal_value= models.BooleanField(
        default= False,
        verbose_name= _("is Normal Value"),
    )

    class Meta:  
        verbose_name= _("Analysis Method Expected Result")
        verbose_name_plural= _("Analysis Method Expected Results")


class AnalysisByCalculatedMethod(AnalysisMethod):
    equation= models.CharField(
        max_length= 25,
        verbose_name= _("Equation"),
    )
    equation_parameters= models.ManyToManyField(
        Parameter,
        through= "EquationParameter",
        verbose_name= _("Equation Parameters"),
    )

    class Meta:
        verbose_name= _("Analysis By Calculated Method")
        verbose_name_plural= _("Analysis By Calculated Methods")


class EquationParameter(models.Model):
    calculated_parameter= models.ForeignKey(
        AnalysisByCalculatedMethod,
        on_delete= models.CASCADE,
        verbose_name= _("Calculated Parameter"),
    )
    equation_parameter= models.ForeignKey(
        Parameter,
        on_delete= models.CASCADE,
        related_name= _("equation_parameters"),
        verbose_name= _("Equation Parameter"),
    )
    symbol_in_equation= models.CharField(
        max_length= 1,
        verbose_name= _("Symbol in Equation"),
    )

    def __str__(self):
        return f"{str(self.calculated_parameter)}->{str(self.equation_parameter)}"

    @property
    def slug(self):
        return self.__str__()

    class Meta:
        unique_together= [
            ["calculated_parameter", "equation_parameter"],
        ]
        verbose_name= _("Equation Parameter")
        verbose_name_plural= _("Equation Parameters")


class AnalysisByTechnique(AnalysisMethod):
    kats = models.ManyToManyField(
        Kat,
        related_name= _("Analysis"),
        verbose_name= _("Kats"),
    )
    run_time= models.CharField(
        max_length= 4,
        choices= Runs.choices,
        verbose_name= _("Run Time"),
    )
    is_available= models.BooleanField(
        default= True,
        verbose_name= _("is Available"),
    )

    class Meta:
        # unique_together = (
        #     "analysis",
        #     "analytical_technique",
        # )
        verbose_name= _("Analysis By Technique")
        verbose_name_plural= _("Analysis By Techniques")


## Lab 2 Lab Menu
class Lab2LabMenu(AnalysisMethod):

    laboratory= models.ForeignKey(
        Facility,
        on_delete= models.CASCADE,
        limit_choices_to = {'facility_type':FacilityTypes.MainLaboratory},
        related_name= _("Analysis"),
        verbose_name= _("Laboratory"),
    )
    run_time= models.CharField(
        max_length= 4,
        choices= Runs.choices,
        verbose_name= _("Run Time"),
    )
    cost= models.FloatField(
        null= True,
        blank= True,
        verbose_name= _("Cost"),
    )  # التكلفه
    reference_range= models.ForeignKey(
        ReferenceRange,
        on_delete= models.CASCADE,
        blank= True,
        null= True,
        related_name= _("Kat_Samples+"),
        verbose_name= _("Reference Range"),
    )

    class Meta:
        # unique_together = [
        #     [
        #         "analysis",
        #         "analysis_by_technique",
        #         "laboratory",
        #     ]
        # ]
        verbose_name= _("Lab2Lab Menu")
        verbose_name_plural= _("Lab2Lab Menus")


class Package(Analysis): # زى التحاليل الشامل
    analysis_in_package= models.ManyToManyField(
        Analysis,
        related_name= _("Package"), 
        verbose_name= _("Analysis in Package"),
    )

    class Meta:
        verbose_name= _("Package")
        verbose_name_plural= _("Packages")


class Senstivity(models.Model):  # ENUM
    class Senstive(models.TextChoices):
        Strong = "Strong"
        Mmderate = "Moderate"
        weak = "Weak"
        very_weak = "Very Weak"

    name = models.CharField(
        max_length=10,
        primary_key=True,
        choices=Senstive.choices,
        verbose_name=_("Name"),
    )

    def __str__(self):
        return str(self.name)

    @property
    def slug(self):
        return slugify(self.name)

    class Meta:
        verbose_name = _("Senstivity")
        verbose_name_plural = _("Senstivites")





#  🧕   🕌   🕋  👳  💲  🌍  👰‍♂️   👰‍♀️   👩‍❤️‍💋‍👩   🤰🏻   🏋️‍♀️   💒   👩‍❤️‍💋‍👨   🧑🏼‍🍼  👩‍🎓   🚣‍♀️  🤾‍♀️  👨‍💼   👷🏽‍♂️  👷🏼‍♀️   👨‍🔧   👨‍⚕  👩🏽‍⚕️  👨🏻‍🎓  👨🏼‍🏫  👩🏽‍🏫   🦷

 