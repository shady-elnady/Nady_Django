from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from GraphQL.models import BaseModelName

# Create your models here.


class Unit(BaseModelName):

    class Measurement(models.TextChoices):
        Package = "PC", _("Package")
        volume = "Vo", _("Volume")
    # TODO Add Info
    class Prefixes(models.TextChoices):
        Giga = "G", _("Giga")
    
    symbol = models.CharField(
        max_length= 5,
        unique= True,
        verbose_name= _("Symbol"),
    )
    prefix = models.CharField(
        max_length= 5,
        null= True,
        blank= True,
        choices= Prefixes.choices,
        verbose_name= _("Prefix"),
    )    
    power = models.SmallIntegerField(
        null=True,
        blank= True,
        verbose_name= _("Power"),
    )
    multiply = models.ForeignKey(
        'self',
        null=True,
        blank= True,
        on_delete=models.CASCADE,
        related_name= _("Multiply_Units"),
        verbose_name=_("Multiply"),
    )
    divide = models.ForeignKey(
        'self',
        null=True,
        blank= True,
        on_delete=models.CASCADE,
        related_name= _("Divide_Units"),
        verbose_name=_("Divide"),
    )
    measurement = models.CharField(
        max_length= 2,
        choices= Measurement.choices,
    )
    convert_to = models.ManyToManyField(
        "self",
        through= "UnitConvert",
        # symmetrical= False,
        verbose_name= _("Convert To"),
    )

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})



class UnitConvert(models.Model):
    from_unit = models.ForeignKey(
        Unit,
        on_delete= models.CASCADE,
        verbose_name= _("from Unit"),
    )
    to_unit = models.ForeignKey(
        Unit,
        on_delete= models.CASCADE,
        related_name= "%(app_label)s_%(class)s_Convert_To",
        verbose_name= _("to Unit"),
    )
    equation = models.CharField(
        max_length= 20,
        null= True,
        blank= True,
        verbose_name= _("Equation"),
    )

    def slug(self):
        return slugify(f"{self.from_unit.name} to {self.to_unit.name}")

    def __str__(self):
        return f"{self.from_unit.name} to {self.to_unit.name}"

    def __decode__(self):
        return f"{self.from_unit.name} to {self.to_unit.name}"

    class Meta:
        unique_together = [["from_unit", "to_unit"]]
        verbose_name = _("Unit Convert")
        verbose_name_plural = _("Units Convert")




# class UnitAtom(BaseModelName):

#     convert_to = models.ManyToManyField(
#         "self",
#         through= "UnitAtomConvert",
#         symmetrical= False,
#         verbose_name= _("Convert To"),
#     )

#     class Meta:
#         verbose_name= _("Unit")
#         verbose_name_plural= _("Units")



# class UnitAtomConvert(models.Model):
#     from_unit = models.ForeignKey(
#         UnitAtom,
#         on_delete= models.CASCADE,
#         verbose_name= _("from UnitAtom"),
#     )
#     to_unit = models.ForeignKey(
#         UnitAtom,
#         on_delete= models.CASCADE,
#         related_name= "%(app_label)s_%(class)s_Convert_To",
#         verbose_name= _("to UnitAtom"),
#     )
#     equation = models.CharField(
#         max_length= 20,
#         null= True,
#         blank= True,
#         verbose_name= _("Equation"),
#     )

#     def slug(self):
#         return slugify(f"{self.from_unit.name} to {self.to_unit.name}")

#     def __str__(self):
#         return f"{self.from_unit.name} to {self.to_unit.name}"

#     def __decode__(self):
#         return f"{self.from_unit.name} to {self.to_unit.name}"

#     class Meta:
#         unique_together = [["from_unit", "to_unit"]]
#         verbose_name = _("UnitAtom Convert")
#         verbose_name_plural = _("UnitAtoms Convert")

