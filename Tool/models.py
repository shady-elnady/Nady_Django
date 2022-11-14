from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from polymorphic.models import PolymorphicModel
from Entity.models import Entity

from GraphQL.models import BaseModelName, BaseModelSVG
from Location.models import Mobile
from Payment.models import Currency

# Create your models here.


class PaymentMethod(BaseModelName, BaseModelSVG):

    class Meta:
        verbose_name= _("Payment Method")
        verbose_name_plural= _("Payment Methods")


# class PhoneCach(models.Model):

#     from_phone= models.ForeignKey(
#         Mobile,
#         limit_choice= {"has_cach": True},
#         on_delete= models.CASCADE,
#         # related_name= _("Sub Categories"),
#         verbose_name= _("from Phone"),
#     )

#     to_phone= models.ForeignKey(
#         Mobile,
#         limit_choice= {"has_cach": True},
#         on_delete= models.CASCADE,
#         # related_name= _("Sub Categories"),
#         verbose_name= _("to Phone"),
#     )

#     class Meta:
#         unique_together = (
#             "from_phone",
#             "to_phone",
#         )
#         verbose_name= _("PhoneCach")
#         verbose_name_plural= _("PhoneCachs")


class Financial(models.Model):
    customer= models.ForeignKey(
        Entity,
        limit_choice= {"has_cach": True},
        on_delete= models.CASCADE,
        related_name= _("Financials"),
        verbose_name= _("Customer"),
    )
    required= models.FloatField(
        verbose_name= _("Required"),
    ) # المطلوب
    is_pure= models.BooleanField(
        default= False,
        verbose_name= _("is Pure"),
    ) # خالص
    currency = models.ForeignKey(
        Currency,
        default= settings.DEFAULT_CURRENCY,
        on_delete= models.CASCADE,
        related_name= _("Financials"),
        verbose_name= _("Currency"),
    )
    payments= models.ManyToManyField(
        PaymentMethod,
        througth= "Payment",
        verbose_name= _("Payments"),
    ) # المدفوع

    @property
    def final_payments(self):
        total = 0
        for payment in self.payments.all():
            total += payment.amount
        return total
    
    class Meta:
        verbose_name= _("Financial")
        verbose_name_plural= _("Financials")


class Payment():
    financial = models.ForeignKey(
        Financial,
        on_delete= models.CASCADE,
        verbose_name= _("Financial"),
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete= models.CASCADE,
        related_name= _("Payments"),
        verbose_name= _("Payment Method"),
    )
    amount= models.FloatField(
        verbose_name= _("Amount"),
    )

    class Meta:
        verbose_name= _("Payment")
        verbose_name_plural= _("Payments")