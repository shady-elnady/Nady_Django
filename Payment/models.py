from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from polymorphic.models import PolymorphicModel

from GraphQL.models import BaseModelName, BaseModelNative, PaymentMethod, PaymentType

# Create your models here.


class Currency(BaseModelNative):
    # code = models.CharField(
    #     max_length=3,
    #     unique=True,
    #     verbose_name=_("Code"),
    # )
    symbol = models.CharField(
        max_length=3,
        unique=True,
        verbose_name=_("Symbol"),
    )
    # equal_dolar = models.FloatField(
    #     blank=True,s
    #     null=True,
    #     verbose_name=_("Equal Dolar"),
    # )
    last_update = models.DateField(
        auto_now=True,
        null=True,
        blank=True,
    )

    # def get_absolute_url(self):
        #     return reverse("_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name= _("Currency")
        verbose_name_plural= _("Currencies")


class RecurringExpenses(BaseModelName): # بنود المصروفات الدوريه

    class ExpenseTimeCyclies(models.TextChoices):
        Daily= "D", _("Daily")
        Weekly= "W", _("Weekly")
        Monthly= "M", _("Monthly")
        Yearly= "Y", _("Yearly")
        Any= "A", _("Any")

    expense_time_cyclie = models.CharField(
        max_length= 2,
        choices= ExpenseTimeCyclies.choices,
        verbose_name= _("Expense Time Cyclie"),
    )
    amount= models.FloatField(
        null= True,
        blank= True,
        verbose_name= _("Amount"),
    )
    currency = models.ForeignKey(
        Currency,
        default= settings.DEFAULT_CURRENCY,
        on_delete= models.CASCADE,
        related_name= _("Financials"),
        verbose_name= _("Currency"),
    )

    class Meta:
        verbose_name= _("Recurring Expense Item")
        verbose_name_plural= _("Recurring Expense Items")


class Payment(PolymorphicModel):
    payment_method= models.CharField(
        max_length= 2,
        choices= PaymentMethod.choices,
        verbose_name= _("Payment Method"),
    )
    charge_id = models.CharField(
        max_length=50,
        unique= True,
        verbose_name= _("Charge ID"),
    )
    currency = models.ForeignKey(
        Currency,
        default= settings.DEFAULT_CURRENCY,
        on_delete= models.CASCADE,
        # related_name= _("Payments"),
        verbose_name= _("Currency"),
    )
    amount = models.FloatField(
        verbose_name= _("Amount"),
    )
    payment_type= models.CharField(
        max_length= 2,
        choices= PaymentType.choices,
        verbose_name= _("Payment Type"),
    )
    payment_date= models.DateTimeField(
        auto_now_add= True,
        editable= False,
        verbose_name= _("Payment Date"),
    )
    
    class Meta:
        verbose_name= _("Payment")
        verbose_name_plural= _("Payments")



# TODO PAYMENT
# class Payment:
#     class PayMethod(models.TextChoices):
#         check = "Check"
#         PayPal = "PayPal"

#     payment_method = models.CharField(max_length=10, choices=PayMethod.choices)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     payment_date = models.DateTimeField(auto_now_add=True)
#     amount = models.DecimalField(max_digits=5, decimal_places=2)  #  المبلغ
#     currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

# TODO CURRENCY API
# https://m3o.com/account/keys

# API_key =  N2Q1OWUwNDctZDM4Ny00MDNkLWIxOGUtYWM1MTJlNGExYTUx

"""
    curl "https://api.m3o.com/v1/currency/Codes" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $M3O_API_TOKEN" \
    -d '{}'
"""

##  https://openexchangerates.org/account/app-ids
# api ID = 82775e187c684ecaa9efc98e7f0e9381



###########################################################################

# class Financial(models.Model, PolymorphicModel):
#     customer= models.ForeignKey(
#         Entity,
#         limit_choice= {"has_cach": True},
#         on_delete= models.CASCADE,
#         related_name= _("Financials"),
#         verbose_name= _("Customer"),
#     )
#     currency = models.ForeignKey(
#         Currency,
#         default= settings.DEFAULT_CURRENCY,
#         on_delete= models.CASCADE,
#         related_name= _("Financials"),
#         verbose_name= _("Currency"),
#     )
#     amount = models.FloatField(
#         verbose_name= _("Amount"),
#     )
#     created_date= models.DateTimeField(
#         auto_now_add=True,
#         editable=False,
#         verbose_name=_("Created Date"),
#     )
    
#     # @property
#     # def final_payments(self):
#     #     total = 0
#     #     for payment in self.payments.all():
#     #         total += payment.amount
#     #     return total
    
#     class Meta:
#         verbose_name= _("Financial")
#         verbose_name_plural= _("Financials")


# class Departed(Financial): # منصرف

#     class Meta:
#         verbose_name= _("Departed")
#         verbose_name_plural= _("Departeds")


