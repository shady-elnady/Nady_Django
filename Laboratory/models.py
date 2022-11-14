from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
import calendar

from polymorphic.models import PolymorphicModel

from GraphQL.models import BaseModel, BaseModelImageOnly, BaseModelName, FacilityTypes, Runs, Scores, upload_to
from GraphQL.custom_fields import QRField
from Payment.models import Currency
from Unit.models import Unit
from Facility.models import Branch, Facility, Shift
from Product.models import Product
from Person.models import Employee, Person, ReferenceLimitingFactor
from Doctor.models import Doctor


# Create your models here.


# TODO Employee Attendance Management System
## https://itsourcecode.com/uml/employee-attendance-management-system-er-diagram-erd/


class Bonuss(models.Model): # المكافاءت
    employee= models.ForeignKey(
        Employee,
        on_delete= models.CASCADE,
        related_name= _("Bonusss"),    # TODO Add to Employee Mpdel
        verbose_name= _("Employee"),
    )
    _date= models.DateTimeField(
        default=now,
        verbose_name=_("Date"),
    )
    amount= models.FloatField(
        verbose_name= _("Amount"),
    )
    reason= models.TextField()

    class Meta:
        verbose_name = _("Bonuss")
        verbose_name_plural = _("Bonusss")


class Deduction(models.Model): # الخصومات
    employee= models.ForeignKey(
        Employee,
        on_delete= models.CASCADE,
        related_name= _("Deductions"),    # TODO Add to Employee Mpdel
        verbose_name= _("Employee"),
    )
    _date= models.DateTimeField(
        default=now,
        verbose_name=_("Date"),
    )
    amount= models.FloatField(
        verbose_name= _("Amount"),
    )
    reason= models.TextField()

    class Meta:
        verbose_name = _("Deduction")
        verbose_name_plural = _("Deductions")


class Vacation(models.Model): # الاجازات
    employee= models.ForeignKey(
        Employee,
        on_delete= models.CASCADE,
        related_name= _("Vacations"),    # TODO Add to Employee Mpdel
        verbose_name= _("Employee"),
    )
    _date= models.DateField(
        verbose_name=_("Date"),
    )
    shift= models.ForeignKey(
        Shift,
        on_delete= models.CASCADE,
        # related_name= _("Vacations"),
        verbose_name= _("Shift"),
    )
    is_accepted= models.BooleanField(
        default= True,
        verbose_name= _("is_Accepted"),
    )

    class Meta:
        verbose_name = _("Vacation")
        verbose_name_plural = _("Vacations")


class Attendance(models.Model):  # الحضور والغياب

    employee= models.ForeignKey(
        Employee,
        on_delete= models.CASCADE,
        related_name= _("Attendances"),    # TODO Add to Employee Mpdel
        verbose_name= _("Employee"),
    )
    attending_time= models.TimeField(
        verbose_name= _("Attending Time"),
    )  # الحضور
    leaving_time= models.TimeField(
        verbose_name= _("Leaving Time"),
    )  # الانصراف

    class Meta:
        verbose_name = _("Laboratory Attendance")
        verbose_name_plural = _("Laboratory Attendances")

###############################################################################################


class Departement(BaseModelName):

    class Meta:
        verbose_name= _("Departement")
        verbose_name_plural= _("Departements")


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
    anti_biotic= unit= models.ForeignKey(
        Product,
        on_delete= models.CASCADE,
        related_name= _("Anti_Biotic_Disks"),
        verbose_name= _("Anti-Biotic"),
    )

    class Meta:
        verbose_name= _("Anti-Biotic Disk")
        verbose_name_plural= _("Anti-Biotic Disks")


#############################################################################################

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
        related_name= _("Analytics"),
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
        related_name= _("Parameters"),
        verbose_name= _("Unit"),
    )
    convert_to_units= models.ManyToManyField(
        "self",
        througth= _("AnalyticsUnitConvert"),
        verbose_name= _("Convert to Units"),
    )
    is_default= models.BooleanField(
        default= True,
        verbose_name= _("Is Default"),
    )   

    def __str__(self):
        return f"{self.analytics.name}->{self.unit.symbol}"

    @property
    def slug(self):
        return slugify(f"{self.analytics.name}->{self.unit.symbol}")

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
        related_name= _("convert_to_units"),
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


###########################################################################################
## Reference Range

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
    reference_range_expected_values= models.ManyToManyField(
        ReferenceLimitingFactor,
        through= "ReferenceRangeExpectedValue",
        verbose_name= _("Reference Range Expected Values"),
    )
    
    class Meta:
        verbose_name= _("Reference Range")
        verbose_name_plural= _("Reference Ranges")


class ReferenceRangeExpectedValue(models.Model):
    reference_range= models.ForeignKey(
        ReferenceRange,
        on_delete= models.CASCADE,
        related_name= _("Reference_Range"), 
        verbose_name= _("ReferenceRange"),
    )
    reference_limiting_factors = models.ManyToManyField(
        ReferenceLimitingFactor,
        related_name= _("+"),
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

###########################################################################


class Kat(LabSupply):
    analytics= models.ForeignKey(
       Analytics,
        on_delete= models.CASCADE,
        related_name= _("Kats"),
        verbose_name= _("Analytics"),
    )
    analytical_technique= models.ForeignKey(
        AnalyticalTechnique,
        related_name= _("Kats"),
        verbose_name= _("Analytical Technique"),
    )
    samples= models.ManyToManyField(
        Specimen,
        through= "KatSample",
        verbose_name= _("Specimens"),
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


###########################################################################


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
        blamk= True,
        on_delete= models.CASCADE,
        related_name= _("Parameters"),
        verbose_name= _("Sample"),
    )
    report= models.ForeignKey(
        Report,
        null= True,
        blank= True,
        related_name= _("Analysis_in_Report"),
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
        # related_name= _("Analysis"),
        verbose_name= _("Analysis"),
    )
    analytical_technique = models.ForeignKey(
        AnalyticalTechnique,
        on_delete= models.CASCADE,
        related_name= _("Analysis"),
        verbose_name= _("Analytical Technique"),
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
    parameter= models.ForeignKey(
        Parameter,
        on_delete= models.CASCADE,
        verbose_name= _("Parameter"),
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
        return f"{str(self.parameter)}->{str(self.equation_parameter)}"

    @property
    def slug(self):
        return self.__str__()

    class Meta:
        uniqe_together= [
            ["parameter", "equation_parameter"],
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
        unique_together = (
            "analysis",
            "analytical_technique",
        )
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
        related_name= _("Kat_Samples"),
        verbose_name= _("Reference Range"),
    )

    class Meta:
        unique_together = [
            [
                "analysis",
                "analysis_by_technique",
                "laboratory",
            ]
        ]
        verbose_name= _("Lab2Lab Menu")
        verbose_name_plural= _("Lab2Lab Menus")


class Package(Analysis): # زى التحاليل الشامل
    analysis_in_package= models.ManyToManyField(
        Analysis,
        # related_name= _("+"), 
        verbose_name= _("Analysis in Package"),
    )

    class Meta:
        verbose_name= _("Package")
        verbose_name_plural= _("Packages")


class Function(Analysis):
    analysis_in_function= models.ManyToManyField(
        Analysis,
        # related_name= _("+"), 
        verbose_name= _("Analysis in Function"),
    )

    class Meta:
        verbose_name= _("Function")
        verbose_name_plural= _("Functions")


class GroupAnalysis(Analysis):
    analysis_in_group= models.ManyToManyField(
        Analysis,
        # related_name= _("+"), 
        verbose_name= _("Analysis in Group"),
    )
    report= models.ForeignKey(
        Report,
        null= True,
        blank= True,
        related_name= _("Analysis_in_Report"),
        verbose_name= _("Report"),
    )

    class Meta:
        verbose_name= _("Group Analysis")
        verbose_name_plural= _("Group Analysis")


class GroupAnalysisImage(Analysis, BaseModelImageOnly):
    group_analysis= models.ForeignKey(
        Analysis,
        on_delete= models.CASCADE,
        related_name= _("Image"), 
        verbose_name= _("Group Analysis"),
    )

    class Meta:
        verbose_name= _("Group Analysis Image")
        verbose_name_plural= _("Group Analysis Images")




###########################################################################################


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


class VitalSign(BaseModelName):   
    """
        vital and sign*
        patient and observation*
        patient and monitoring Second search terms include:
        heart rate AND (determin* OR measure*)
        blood pressure AND (determin* OR measure*)
        body temperature AND (determin* OR measure*)
        respiratory rate AND (determin* OR measure*)
        vital signs AND (determin* OR measure*)
        fifth vital sign AND (determin* OR measure*)
        monitoring AND physiological AND/OR nursing
        pulse AND evaluat*
        pulse oximetry AND (determin* OR measure*)
        patient oxygenation AND (determin* OR measure*)
        pain AND vital sign (determin* OR measure*)
        blood and pressure in ti
        respirat* in ti
        pulse in ti
        temperature in ti
        vital and sign* in ti
        observation* in ti.
        fasting. / postprandial

        حيوية وعلامة *
        المريض والمراقبة *
        تتضمن مصطلحات البحث الثانية الخاصة بالمريض والمراقبة ما يلي:
        معدل ضربات القلب و (تحديد * أو قياس *)
        ضغط الدم و (تحديد * أو قياس *)
        درجة حرارة الجسم و (تحديد * أو قياس *)
        معدل التنفس و (تحديد * أو قياس *)
        العلامات الحيوية و (تحديد * أو قياس *)
        العلامة الحيوية الخامسة AND (تحديد * أو قياس *)
        المراقبة و / أو الفسيولوجية و / أو التمريض
        نبض وتقييم *
        قياس النبض و (تحديد * أو قياس *)
        أكسجة المريض و (تحديد * أو قياس *)
        الألم والعلامة الحيوية (تحديد * أو قياس *)
        الدم والضغط في تي
        تنفس * في ti
        نبض في ti
        درجة الحرارة في تي
        الحيوية وتسجيل الدخول ti
        المراقبة * في ti
        صاءم او فاطر
    """
    max_value = models.FloatField(
        blank= True,
        null= True,
        verbose_name=_("Maximum Value"),
    )
    min_value = models.FloatField(
        blank= True,
        null= True,
        verbose_name=_("Minimum Value"),
    )
    low_normal_value = models.FloatField(
        blank= True,
        null= True,
        verbose_name=_("Low Normal Value"),
    )
    high_normal_value = models.FloatField(
        blank= True,
        null= True,
        verbose_name=_("High Normal Value"),
    )
    unit = models.ForeignKey(
        Unit,
        on_delete= models.CASCADE,
        blank= True,
        null= True,
        related_name= _("Vital_Signs"),
        verbose_name= _("Unit"),
    )

    class Meta:
        verbose_name = _("Vital Sign")
        verbose_name_plural = _("Vital Signs")


class Prescription(BaseModelImageOnly, BaseModel): # الروشتات
    qr_code= QRField(
        primary_key= True,
        verbose_name= _("Prescription QR Code"),
    )
    branch= models.ForeignKey(
        Branch,
        on_delete= models.CASCADE,
        related_name= _("Prescriptions"),
        verbose_name= _("Branch"),
    )
    patient= models.ForeignKey(
        Person,
        on_delete= models.CASCADE,
        related_name= _("Prescriptions"),
        verbose_name= _("Patient"),
    )
    treating_doctor= models.ForeignKey(
        Doctor,
        on_delete= models.CASCADE,
        blank= True,
        null= True,
        related_name= _("Prescriptions"),
        verbose_name= _("Treating Doctor"),
    )
    transfer_destination= models.ForeignKey(
        Facility,
        on_delete= models.CASCADE,
        blank= True,
        null= True,
        limit_choices_to= {"facility_type": FacilityTypes.Dispensary_Associations},
        related_name= _("Prescriptions"),
        verbose_name= _("Transfer Destination"),
    ) # جهةالتحويل
    visits= models.ManyToManyField(
        Employee,
        through= "Visit",
        verbose_name= _("Visits"),
    )
    required_in_date= models.DateTimeField(
        default= now,
        editable= True,
        verbose_name= _("Required in Date"),
    )
    is_reservation= models.BooleanField(
        default= False,
        verbose_name= _("is Reservation"),
    ) # حجز
    expected_receipt_time= models.DateTimeField(
        null= True,
        blank= True,
        verbose_name= _("Expected Receipt Time"),
    ) # وقت الاستلام المتوقع
    cost= models.FloatField(
        verbose_name= _("Cost"),
    )
    discount= models.FloatField(
        default= 0,
        verbose_name= _("Discount"),
    )
    currency = models.ForeignKey(
        Currency,
        default= settings.DEFAULT_CURRENCY,
        on_delete= models.CASCADE,
        # related_name= _("Prescriptions"),
        verbose_name= _("Currency"),
    )

    # @property
    # def all_required_analysis(self) -> list:
    #     all_analysis= []
    #     for visit in self.visits.all():
    #         for VisitAnalysis in visit.required_analysis.all():
    #             all_analysis.append(VisitAnalysis.analysis)
    #     return all_analysis
    
    class Meta:
        verbose_name= _("Prescription")
        verbose_name_plural= _("Prescriptions")


class Visit(models.Model):
    prescription= models.ForeignKey(
        Prescription,
        on_delete= models.CASCADE,
        # related_name= _("Visits"),
        verbose_name= _("Prescription"),
    )
    # TODO Employee Activity
    employee= models.ManyToManyField(
        Employee,
        through= "EmployeeActivity",
        verbose_name= _("Employee"),
    )
    external_phlebotomy= models.ForeignKey(
        Employee,
        on_delete= models.SET("Deleted"),
        null= True,
        blank= True,
        related_name= _("Visit_External_Phlebotomy"),
        verbose_name= _("External Phlebotomy"),
    ) # سحب خارجى
    visit_patient_vital_Signs= models.ManyToManyField(
        VitalSign,
        through= "VisitPatientVitalSign",
        verbose_name= _("Visit Patient Vital Signs"),
    ) # المؤشرات الحيويه للمريض بالزياره
    required_analysis= models.ManyToManyField(
        Analysis,
        through= "VisitAnalysis",
        related_name= _("Visits"),
        verbose_name= _("Required Analysis"),
    )
    phlebotomy_time= models.DateTimeField(
        default= now,
        editable= True,
        verbose_name= _("Phlebotomy Time"),
    ) # وقت السحب

    class Meta:
        verbose_name= _("Visit")
        verbose_name_plural= _("Visits")


############################################################################################################################################

class VisitAnalysis(models.Model):

    class ResultDescription(models.TextChoices):
        Low= "L", _("Low")
        Normal= "N", _("Normal")
        High= "H", _("High")
    
    visit= models.ForeignKey(
        Visit,
        on_delete= models.CASCADE,
        # related_name=_("%(app_label)s_%(class)s_Visit"),
        verbose_name= _("Visit"),
    )
    analysis= models.ForeignKey(
        Analysis,
        on_delete= models.CASCADE,
        related_name= _("Visits"),
        verbose_name= _("Analysis"),
    )
    result= models.CharField(
        max_length= 20,
        verbose_name= _("Result"),
    )
    is_= models.BooleanField(
        default= False,
        verbose_name= _("Result"),
    ) # هل تم المراجعه
    is_= models.BooleanField(
        default= False,
        verbose_name= _("Result"),
    ) # هل تم التسليم للمريض
    result_description= models.CharField(
        max_length= 2,
        null= True,
        blank= True,
        choices= ResultDescription.choices,
        verbose_name= _("Result Description"),
    )

    class Meta:
        unique_together= [
            ["visit", "analysis"],
        ]
        verbose_name= _("Visit Analysis")
        verbose_name_plural= _("Visits Analysis")


############################################################################################################################################

class LineInReport(models.Model):
    group_in_report = models.ForeignKey(
        GroupInVisitReport,
        on_delete=models.CASCADE,
        verbose_name=_("Group In Report"),
        related_name=_("%(app_label)s_%(class)s_Group_In_Report"),
    )
    analysis = models.ForeignKey(
        Analysis,
        on_delete=models.CASCADE,
        verbose_name=_("Analysis"),
        related_name=_("%(app_label)s_%(class)s_Analysis"),
    )
    value = 
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name=_("Unit"),
        related_name=_("%(app_label)s_%(class)s_Unit"),
    )
    normal_range = models.ForeignKey(
        NormalRange,
        on_delete=models.CASCADE,
        verbose_name=_("Unit"),
        related_name=_("%(app_label)s_%(class)s_Unit"),
    )

    @property
    def unit(self):
        return self.analysis.unit

    def __str__(self):
        return f"{str(self.group_in_report)}->{str(self.analysis)}"

    @property
    def slug(self):
        return slugify(self.__str__)

    class Meta:
        unique_together = [["group_in_report", "analysis"]]
        verbose_name = _("Line In Report")
        verbose_name_plural = _("Lines In Reports")


############################################################################################################################################


class VisitPatientVitalSign(models.Model):  # المؤشرات الحيويه للمريض اثناء الزياره
    visit= models.ForeignKey(
        Visit,
        on_delete= models.CASCADE,
        related_name= _("vital_Signs"),
        verbose_name= _("Visit"),
    )
    vital_sign= models.ForeignKey(
        VitalSign,
        on_delete= models.CASCADE,
        related_name= _("Visits"),
        verbose_name= _("Vital Sign"),
    )
    value= models.FloatField(
        verbose_name= _("Value"),
    )

    class Meta:
        unique_together= [
            ["visit", "vital_sign"],
        ]
        verbose_name= _("Visit Patient Vital Sign")
        verbose_name_plural= _("Visit Patient Vital Signs")



########################################################################################################################
## Employee Activity


class EmployeeActivity(models.Model):
    class Activity(models.TextChoices):
        Print = "Print"

    employee = models.ForeignKey(
       Employee,
        on_delete=models.CASCADE,
        verbose_name=_("Employee"),
        related_name=_("%(app_label)s_%(class)s_Employee"),
    )
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        verbose_name=_("Visit"),
        related_name=_("%(app_label)s_%(class)s_Visit"),
    )
    activity = models.CharField(
        max_length=5,
        choices=Activity.choices,
        verbose_name=_("Activity"),
    )
    execution_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Execution Time"),
    )

    def __str__(self):
        return f"{str(self.employee)}->{str(self.visit)}"

    @property
    def slug(self):
        return slugify(f"{str(self.employee)}->{str(self.visit)}")

    class Meta:
        unique_together = [["employee", "visit", "activity"]]
        verbose_name = _("Employee Activity")
        verbose_name_plural = _("Employee Activitys")



#############################################################################
## inventory management  ادارة المخزون

class Stock(BaseModel):  # المخزون
    lab_supply = models.OneToOneField(
        LabSupply,
        on_delete=models.CASCADE,
        verbose_name=_("Laboratory Supply"),
    )
    # TODO PRODUCT DEATAILS STOCK
    product_details = models.ManyToManyField(
        LineInInvoice,
        verbose_name=_("Product Details"),
        related_name="%(app_label)s_%(class)s_Product_Details",
    )

    @property
    def packing(self):
        return self.lab_supply.default_packing

    @property  # inventory  المخزون
    def stock(self):
        return sum(list(map(lambda x: x["count_packing"], self.product_details)))

    class Meta:
        verbose_name = _("Stock")
        verbose_name_plural = _("Stocks")

    def __str__(self):
        return str(self.product)

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})

######################################################################################################################