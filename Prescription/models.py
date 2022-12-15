from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from Analysis.models import Analysis, AnalysisMethod, GroupAnalysis, Report
from Doctor.models import Doctor
from Employee.models import Employee
from Facility.models import Branch, Facility
from django.utils.timezone import now

from GraphQL.models import BaseModel, BaseModelImageOnly, BaseModelName, FacilityTypes
from GraphQL.custom_fields import BarCodeField, QRField
from Payment.models import Payment
from Person.models import Person
from Specimen.models import Specimen
from Unit.models import Unit

# Create your models here.


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
    BaeC= BarCodeField()
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
        blank= True,
        null= True,
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

