from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from GraphQL.models import BaseModelName
from Person.models import Person

# Create your models here.




   



class Doctor(Person):
    
    class MedicalSpecialization(models.TextChoices):
        Childern= "Ch", _("Childern")
    
    medical_specialization = models.CharField(
        max_length= 4,
        choices= MedicalSpecialization.choices,
        verbose_name= _("Medical Specialization"),
    )

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")
