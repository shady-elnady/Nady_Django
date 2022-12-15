from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from djongo.models import ArrayReferenceField
from polymorphic.models import PolymorphicModel
from Analysis.models import Report
from Employee.models import Employee

from GraphQL.models import BaseModel, BaseModelImageOnly, BaseModelName, FacilityTypes, Runs, Scores, upload_to
from GraphQL.custom_fields import BarCodeField, QRField
from Kat.models import LabSupply
from Parameters.models import Analytics
from Payment.models import Payment
from Prescription.models import Phlebotomy, Prescription, PrescriptionPayment
from Specimen.models import Sample
from Unit.models import Unit
from Facility.models import Branch, Facility, Shift
from Product.models import LineInInvoice, Product
from Person.models import Person, ReferenceLimitingFactor
from Doctor.models import Doctor

# Create your models here.


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
