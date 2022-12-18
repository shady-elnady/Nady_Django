from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from polymorphic.models import PolymorphicModel

from GraphQL.models import BaseModel, BaseModelName
from Invoice.models import LineInInvoice
from Analysis.models import Report
from Employee.models import Employee
from Kat.models import LabSupply
from Prescription.models import Phlebotomy, Prescription, PrescriptionPayment

# Create your models here.


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
