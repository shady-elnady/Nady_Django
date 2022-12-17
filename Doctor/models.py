from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from djongo.models import ArrayReferenceField

from GraphQL.models import MedicalSpecialties
from Facility.models import Facility
from Person.models import Person

# Create your models here.


class Doctor(Person):    
    nick_name= models.CharField(
        max_length= 25,
        unique= True,
        verbose_name= _("Nick Name"),
    ) # أسم الشهره
    medical_specialty= models.CharField(
        max_length= 4,
        choices= MedicalSpecialties.choices,
        verbose_name= _("Medical Specialty"),
    )
    private_clinics= ArrayReferenceField(
        to= "PrivateClinic",
    )

    class Meta:
        verbose_name= _("Doctor")
        verbose_name_plural= _("Doctors")


class PrivateClinic(Facility):
    owner_doctor= models.ForeignKey(
        Doctor,
        on_delete= models.CASCADE,
        related_name= _("Facilities"),
        verbose_name= _("Owner's Doctor"),
    )

    class Meta:
        verbose_name= _("Private Clinic")
        verbose_name_plural= _("Private Clinics")