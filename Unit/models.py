from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from polymorphic.models import PolymorphicModel

from GraphQL.models import BaseModelNative, Measurements

# Create your models here.


class Prefix(BaseModelNative):
    symbol= models.CharField(
        max_length= 2,
        unique= True,
        verbose_name= _("Symbol"),
    )
    power= models.IntegerField(
        verbose_name= _("Power"),
    ) 

    def slug(self):
        return slugify(f"{self.symbol}")

    def __str__(self):
        return f"{self.symbol}"

    def __decode__(self):
        return f"{self.symbol}"

    class Meta:
        verbose_name= _("Prefix")
        verbose_name_plural= _("Prefixes")


class Unit(PolymorphicModel, BaseModelNative):
    
    symbol= models.CharField(
        max_length= 5,
        unique= True,
        verbose_name= _("Symbol"),
    )
    measurement= models.CharField(
        max_length= 2,
        choices= Measurements.choices,
        verbose_name= _("Measurement"),
    )
    convert_to= models.ManyToManyField(
        "self",
        through= "UnitConvert",
        symmetrical= True,
        verbose_name= _("Convert To"),
    )

    def slug(self):
        return slugify(f"{self.symbol}")

    def __str__(self):
        return f"{self.symbol}"

    def __decode__(self):
        return f"{self.symbol}"

    class Meta:
        verbose_name= _("Unit")
        verbose_name_plural= _("Units")

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class UnitSystem(Unit):
    system_name= models.CharField(
        max_length= 20,
        verbose_name= _("System Name"),
    )

    class Meta:
        verbose_name= _("Unit System")
        verbose_name_plural= _("Units Systems")


class ComplexUnit(Unit):
    prefix= models.ForeignKey(
        Prefix,
        null= True,
        blank= True,
        on_delete= models.CASCADE,
        related_name= _("Units"),
        verbose_name= _("Prefix"),
    )
    power= models.SmallIntegerField(
        null= True,
        blank= True,
        verbose_name= _("Power"),
    )
    multiply= models.ForeignKey(
        Unit,
        null= True,
        blank= True,
        on_delete= models.CASCADE,
        related_name= _("Multiply_Units"),
        verbose_name= _("Multiply"),
    )
    divide= models.ForeignKey(
        Unit,
        null= True,
        blank= True,
        on_delete= models.CASCADE,
        related_name= _("Divide_Units"),
        verbose_name= _("Divide"),
    )

    class Meta:
        verbose_name= _("Complex Unit")
        verbose_name_plural= _("Complex Units")


class UnitConvert(models.Model):
    unit= models.ForeignKey(
        Unit,
        on_delete= models.CASCADE,
        verbose_name= _("Unit"),
    )
    to_unit= models.ForeignKey(
        Unit,
        on_delete= models.CASCADE,
        related_name= _("%(app_label)s_%(class)s_Convert_To+"),
        verbose_name= _("to Unit"),
    )
    equation= models.CharField(
        max_length= 20,
        null= True,
        blank= True,
        verbose_name= _("Equation"),
    )

    def slug(self):
        return slugify(f"{self.unit.symbol} to {self.to_unit.symbol}")

    def __str__(self):
        return f"{self.unit.symbol} to {self.to_unit.symbol}"

    def __decode__(self):
        return f"{self.unit.symbol} to {self.to_unit.symbol}"

    class Meta:
        unique_together= [
            ["unit", "to_unit"],
        ]
        verbose_name= _("Unit Convert")
        verbose_name_plural= _("Units Convert")
