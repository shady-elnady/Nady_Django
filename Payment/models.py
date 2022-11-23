from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from polymorphic.models import PolymorphicModel
# from djmoney.models.fields import MoneyField
# from djmoney.money import Money
# from djmoney.models.validators import MaxMoneyValidator,MinMoneyValidator
from GraphQL.models import BaseModelName, BaseModelNative, PaymentMethod

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


class FinancialItem(BaseModelName): # بنود ماليه 

    class FinancialItemTypes(models.TextChoices):
        RevenueItem= "R", _("Revenue Item")
        ExpenseItem= "E", _("Expense Item")

    item_type= models.CharField(
        max_length= 1,
        choices= FinancialItemTypes.choices,
        verbose_name= _("Financial Item Type"),
    )

    class Meta:
        verbose_name= _("Financial Item")
        verbose_name_plural= _("Financial Items")


class PeriodicFinancialItem(models.Model): # البنود الماليه الدوريه
    
    class FinancialPeriodicTimes(models.TextChoices):
        Daily= "D", _("Daily")
        Weekly= "W", _("Weekly")
        Monthly= "M", _("Monthly")
        Yearly= "Y", _("Yearly")
        Any= "A", _("Any")
    
    item= models.ForeignKey(
        FinancialItem,
        on_delete= models.CASCADE,
        # related_name= _("Financials"),
        verbose_name= _("Financial Item"),
    )
    periodic_time = models.CharField(
        max_length= 2,
        choices= FinancialPeriodicTimes.choices,
        verbose_name= _("Periodic Time"),
    )
    amount= models.FloatField(
        verbose_name= _("Amount"),
    )
    # amount= MoneyField(
    #     max_digits=settings.CURRENCY_MAX_DIGITS,
    #     decimal_places=settings.CURRENCY_DECIMAL_PLACES,
    #     default_currency=settings.BASE_CURRENCY,
    #     null=True,
    #     blank=True,
    #     validators=[
    #         MinMoneyValidator(10),
    #         MaxMoneyValidator(1500),
    #         MinMoneyValidator(Money(500,'NOK')),
    #         MaxMoneyValidator(Money(900,'NOK')),
    #         MinMoneyValidator({'EUR':100,'USD':50}),
    #         MaxMoneyValidator({'EUR':1000,'USD':500}),
    #     ]
    # )
    currency= models.ForeignKey(
        Currency,
        default= settings.DEFAULT_CURRENCY,
        on_delete= models.CASCADE,
        related_name= _("Financials"),
        verbose_name= _("Currency"),
    )

    class Meta:
        verbose_name= _("Periodic Financial Item")
        verbose_name_plural= _("Periodic Financial Items")


class Payment(PolymorphicModel):
    financial_item= models.ForeignKey(
        FinancialItem,
        null= True,
        blank= True,
        on_delete= models.CASCADE,
        related_name= _("Payments"),
        verbose_name= _("FinancialItem"),
    )
    payment_method= models.CharField(
        max_length= 2,
        choices= PaymentMethod.choices,
        verbose_name= _("Payment Method"),
    )
    charge_id= models.CharField(
        max_length=50,
        unique= True,
        verbose_name= _("Charge ID"),
    )
    currency= models.ForeignKey(
        Currency,
        default= settings.DEFAULT_CURRENCY,
        on_delete= models.CASCADE,
        related_name= _("Payments"),
        verbose_name= _("Currency"),
    )
    amount= models.FloatField(
        verbose_name= _("Amount"),
    )
    payment_time= models.DateTimeField(
        auto_now_add= True,
        editable= False,
        verbose_name= _("Payment Time"),
    )
    
    class Meta:
        verbose_name= _("Payment")
        verbose_name_plural= _("Payments")


class PeriodicPayment(Payment):
    periodic_financial_item= models.ForeignKey(
        PeriodicFinancialItem,
        on_delete= models.CASCADE,
        related_name= _("Payments"),
        verbose_name= _("Periodic Financial Item"),
    )

    # def save(self, *args, **kwargs):
    #     super(PeriodicPayment, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name= _("Periodic Item")
        verbose_name_plural= _("Periodic Items")


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


