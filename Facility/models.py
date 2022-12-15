from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from polymorphic.models import PolymorphicModel

from GraphQL.models import (
    BaseModel,
    BaseModelImage,
    BaseModelName,
    DayParts,
    FacilityTypes,
    WeekDays,
)
from Entity.models import Entity
from Location.models import Country

# Create your models here.


class Facility(Entity):  # منشاءت
    owner = models.ForeignKey(
        to="Person.Person",
        on_delete= models.CASCADE,
        related_name= _("Facilities"),
        verbose_name=_("Owner"),
    )
    facility_type = models.CharField(
        max_length= 35,
        choices= FacilityTypes.choices,
        verbose_name=_("Facility Type"),
    )

    class Meta:
        verbose_name = _("Facility")
        verbose_name_plural = _("Facilities")


class Store(BaseModelName):  # مخازن

    owner_facility = models.ForeignKey(
        Facility,
        on_delete= models.CASCADE,
        related_name= _("Stores"),
        verbose_name= _("Owner Facility"),
    )

    class Meta:
        verbose_name = _("Store")
        verbose_name_plural = _("Stores")


class Branch(Entity, BaseModel):

    owning_facility = models.ForeignKey(
        Facility,
        on_delete= models.CASCADE,
        related_name= _("Branchs"),
        verbose_name= _("Owning Facility"),
    )    

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branchs")


class MobileNetWork(Facility):  # شركات محمول

    tel_code = models.CharField(
        max_length= 5,
        blank= True,
        null= True,
        unique= True,
        verbose_name= _("Telephone Code"),
    )

    class Meta:
        verbose_name = _("Mobile NetWork")
        verbose_name_plural = _("Mobile NetWorks")



class Brand(BaseModelImage):
    made_in= models.ForeignKey(
        Country,
        null= True,
        blank= True,
        on_delete= models.CASCADE,
        related_name= _("Made Brands+"),
        verbose_name= _("Made In"),
    )

    class Meta:
        verbose_name= _("Brand")
        verbose_name_plural= _("Brands")


class Departement(BaseModelName):

    class Meta:
        verbose_name= _("Departement")
        verbose_name_plural= _("Departements")


class Shift(PolymorphicModel, BaseModel):  # شفتات ايام الاسبوع

    week_day = models.CharField(
        max_length= 10,
        choices= WeekDays.choices,
        verbose_name= _("Week Day"),
    )
    day_part = models.CharField(
        max_length=4,
        choices=DayParts.choices,
        verbose_name= _("Day Part"),
    )
    attending_time = models.TimeField(
        verbose_name= _("Attending Time"),
    )  # الحضور
    leaving_time = models.TimeField(
        verbose_name= _("Leaving Time"),
    )  # الانصراف

    @property
    def name(self):
        return f"{self.week_day} - {self.day_part}"

    @property
    def slug(self):
        return slugify(f"{self.week_day} - {self.day_part}")

    def __str__(self):
        return f"{self.week_day} - {self.day_part}"

    @property
    def shift_hours(self):
        return self.leaving_time - self.attending_time

    class Meta:
        unique_together = [["week_day", "day_part"]]
        verbose_name = _("Shift")
        verbose_name_plural = _("Shifts")


class Job(BaseModelName):
    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})