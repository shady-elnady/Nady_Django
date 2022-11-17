from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from djongo.models import ArrayReferenceField
from polymorphic.models import PolymorphicModel

from GraphQL.models import BaseModel, BaseModelImageOnly, BaseModelName, FacilityTypes, Runs, Scores, upload_to
from GraphQL.custom_fields import QRField
from Payment.models import Payment
from Unit.models import Unit
from Facility.models import Branch, Facility, Shift
from Product.models import LineInInvoice, Product
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
    anti_biotic= models.ForeignKey(
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
    receptionist= models.ManyToManyField(
        Employee,
        through= "PrescriptionEmployeeActivity",
        verbose_name= _("Receptionist"),
    ) # موظف الاستقبال
    treating_doctor= models.ForeignKey(
        Doctor,
        on_delete= models.CASCADE,
        blank= True,
        null= True,
        related_name= _("Writed_Prescriptions"),
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
    phlebotomy_required_time= models.DateTimeField(
        default= now,
        editable= True,
        verbose_name= _("Phlebotomy Required Time"),
    ) # الوقت المطلوب للسحب
    expected_receipt_time= models.DateTimeField(
        null= True,
        blank= True,
        verbose_name= _("Expected Receipt Time"),
    ) # وقت الاستلام المتوقع
    discount= models.FloatField(
        default= 0,
        verbose_name= _("Discount"),
    )
    prescription_vital_Signs= models.ManyToManyField(
        VitalSign,
        through= "PrescriptionVitalSign",
        verbose_name= _("Prescription Vital Signs"),
    ) # المؤشرات الحيويه للمريض بالزياره
    # payments= models.ManyToManyField(
    #     Payment,
    #     through= "PrescriptionPayment",
    #     verbose_name= _("Payments"),
    # )

    # @property
    # cost

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


class Phlebotomy(models.Model):
    prescription= models.ForeignKey(
        Prescription,
        on_delete= models.CASCADE,
        related_name= _("Phlebotomy_Sessions"),
        verbose_name= _("Prescription"),
    )
    required_analysis= models.ManyToManyField(
        AnalysisMethod,
        # through= "",
        # related_name= _("+"),
        verbose_name= _("Required Analysis"),
    )
    specimens= models.ManyToManyField(
        Specimen,
        through= "PhlebotomySpecimen",
        related_name= _("Phlebotomys"),
        verbose_name= _("Specimens"),
    )
    phlebotomists= models.ManyToManyField(
        Employee,
        through= "PhlebotomyEmployeeActivity",
        verbose_name= _("Phlebotomist"),
    ) # فنى سحب دم
    # TODO Employee Activity
    phlebotomy_time= models.DateTimeField(
        default= now,
        editable= True,
        verbose_name= _("Phlebotomy Time"),
    ) # وقت السحب
    is_external_phlebotomy= models.BooleanField(
        default= False,
        verbose_name= _("is Phlebotomy Time"),
    )

    class Meta:
        verbose_name= _("Prescription")
        verbose_name_plural= _("Prescriptions")


class PhlebotomySpecimen(models.Model):
    phlebotomy= models.ForeignKey(
        Phlebotomy,
        on_delete= models.CASCADE,
        verbose_name= _("Phlebotomy"),
    )
    specimen= models.ForeignKey(
        Specimen,
        on_delete= models.CASCADE,
        verbose_name= _("Specimen"),
    )
    is_take_outSide= models.BooleanField(
        default= False,
        verbose_name= _("is Taken Out Side"),
    )

    class Meta:
        unique_together= [
            ["phlebotomy", "specimen"],
        ]
        verbose_name= _("Phlebotomy Specimen")
        verbose_name_plural= _("Phlebotomy Specimens")



############################################################################################################################################
# Payment
class PrescriptionPayment(Payment):
    prescription= models.ForeignKey(
        Prescription,
        on_delete= models.CASCADE,
        related_name= _("Payments"),
        verbose_name= _("Prescription"),
    )
    
    class Meta:
        verbose_name= _("Prescription Payment")
        verbose_name_plural= _("Prescription Payments")


############################################################################################################################################

class PrescriptionReport(models.Model):
    prescription= models.ForeignKey(
        Prescription,
        on_delete= models.CASCADE,
        related_name= _("Reports"),
        verbose_name= _("Prescription"),
    )
    report= models.ForeignKey(
        Report,
        on_delete= models.CASCADE,
        # related_name= _("+"),
        verbose_name= _("Report"),
    )
    comment= models.CharField(
        max_length= 250,
        null= True,
        blank= True,
        verbose_name= _("Comment"),
    )
    # employee_activities= models.ManyToManyField(
    #     Employee,
    #     through= "ReportEmployeeActivity",
    #     # related_name= _("+"),
    #     verbose_name= _("Employee Activities"),
    # )

    class Meta:
        verbose_name= _("Prescription Report")
        verbose_name_plural= _("Prescription Reports")

############################################################################################################################################

class LineInReport(models.Model):
    analysis= models.ForeignKey(
        AnalysisMethod,
        on_delete= models.CASCADE,
        related_name= _("%(app_label)s_%(class)s_Analysis"),
        verbose_name= _("Analysis"),
    )
    group= models.ForeignKey(
        GroupAnalysis,
        on_delete= models.CASCADE,
        null= True,
        blank= True,
        # related_name= _("prescription_Parameters"),
        verbose_name= _("Group"),
    )
    super_analysis= models.ForeignKey(
        "self",
        on_delete= models.CASCADE,
        related_name= _("Sub_Analysis"),
        verbose_name= _("Super Analysis"),
    )
    result= models.CharField(
        max_length= 40,
        verbose_name= _("Result"),
    )

    class Meta:
        verbose_name = _("Line In Report")
        verbose_name_plural = _("Lines In Reports")


class PrescriptionReportImage(Analysis, BaseModelImageOnly):
    prescription_report= models.ForeignKey(
        PrescriptionReport,
        on_delete= models.CASCADE,
        related_name= _("Images"), 
        verbose_name= _("Prescription Report"),
    )

    class Meta:
        verbose_name= _("Prescription Report Image")
        verbose_name_plural= _("Prescription Report Images")

############################################################################################################################################


class PrescriptionVitalSign(models.Model):  # المؤشرات الحيويه للمريض اثناء الزياره
    prescription= models.ForeignKey(
        Prescription,
        on_delete= models.CASCADE,
        # related_name= _("vital_Signs"),
        verbose_name= _("Prescription"),
    )
    vital_sign= models.ForeignKey(
        VitalSign,
        on_delete= models.CASCADE,
        related_name= _("Prescriptions"),
        verbose_name= _("Vital Sign"),
    )
    value= models.FloatField(
        verbose_name= _("Value"),
    )

    class Meta:
        unique_together= [
            ["prescription", "vital_sign"],
        ]
        verbose_name= _("Prescription Vital Sign")
        verbose_name_plural= _("Prescription Vital Signs")



########################################################################################################################
## Employee Activity
class Activity(BaseModelName):
    
    class Meta:
        verbose_name= _("Activity")
        verbose_name_plural= _("Activities")


class EmployeeActivity(PolymorphicModel):
    employee= models.ForeignKey(
       Employee,
        on_delete= models.CASCADE,
        verbose_name= _("Employee"),
    )
    activity= models.ForeignKey(
       Activity,
        on_delete= models.CASCADE,
        blank= True,
        null= True,
        related_name= _("Employee_Activities"),
        verbose_name= _("Activity"),
    )
    execution_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Execution Time"),
    )

    class Meta:
        verbose_name= _("Employee Activity")
        verbose_name_plural= _("Employee Activities")


class ReportEmployeeActivity(EmployeeActivity):
    report= models.ForeignKey(
       Report,
        on_delete= models.CASCADE,
        related_name= _("Employee_Activities"),
        verbose_name= _("Report"),
    )

    class Meta:
        verbose_name= _("Report Employee Activity")
        verbose_name_plural= _("Report Employee Activities")


class PrescriptionEmployeeActivity(EmployeeActivity):
    prescription= models.ForeignKey(
        Prescription,
        on_delete= models.CASCADE,
        related_name= _("%(app_label)s_%(class)s_Visit"),
        verbose_name= _("Prescription"),
    )

    class Meta:
        verbose_name= _("Prescription Employee Activity")
        verbose_name_plural= _("Prescription Employee Activities")


class PhlebotomyEmployeeActivity(EmployeeActivity):
    phlebotomy= models.ForeignKey(
        Phlebotomy,
        on_delete= models.CASCADE,
        related_name= _("phlebotomists+"),
        verbose_name= _("Phlebotomy"),
    )

    class Meta:
        verbose_name= _("Phlebotomy Employee Activity")
        verbose_name_plural= _("Phlebotomy Employee Activities")


class PaymentEmployeeActivity(EmployeeActivity):
    phlebotomy= models.ForeignKey(
        PrescriptionPayment,
        on_delete= models.CASCADE,
        related_name= _("phlebotomists"),
        verbose_name= _("Phlebotomy"),
    )

    class Meta:
        verbose_name= _("Payment Employee Activity")
        verbose_name_plural= _("Payment Employee Activities")


#############################################################################
## inventory management  ادارة المخزون

class Stock(BaseModel):  # المخزون
    lab_supply= models.OneToOneField(
        LabSupply,
        on_delete= models.CASCADE,
        verbose_name= _("Laboratory Supply"),
    )
    product_details= models.ManyToManyField(
        LineInInvoice,
        related_name= _("Stocks"),
        verbose_name= _("Product Details"),
    )

    @property  # inventory  المخزون
    def stock(self):
        return sum(list(map(lambda x: x["count_packing"], self.product_details)))

    def __str__(self):
        return str(self.lab_supply.name)
    
    class Meta:
        verbose_name= _("Stock")
        verbose_name_plural= _("Stocks")

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})
