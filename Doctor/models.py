from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from GraphQL.models import BaseModelName
from Person.models import Person

# Create your models here.


class Doctor(Person):
    
    class MedicalSpecialties(models.TextChoices): # تخصصات الاطباء
        Childern= "Ch", _("Childern")
    
    nick_name= models.CharField(
        max_length= 25,
        unique= True,
        verbose_name= _("Nick Name"),
    ) # أسم الشهره
    medical_specialty = models.CharField(
        max_length= 4,
        choices= MedicalSpecialties.choices,
        verbose_name= _("Medical Specialty"),
    )

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")
