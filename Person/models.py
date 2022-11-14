from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from datetime import date
import calendar

from polymorphic.models import PolymorphicModel

from GraphQL.models import  BaseModelEmoji
from Entity.models import Entity
from Language.models import Language
from Facility.models import Branch, Job, Shift


# Create your models here.

class Age :
    year :int
    month :int
    day :int
    def __init__(self, year=0, month=0, day=0, *args, **kwargs):
        self.year = year
        self.month = month
        self.day = day
        super(Age, self).__init__(year, month, day, *args, **kwargs)
    

class ReferenceLimitingFactor(PolymorphicModel, BaseModelEmoji):
    category = models.ForeignKey(
        "self",
        on_delete= models.CASCADE,
        related_name= _("Sub_Category"),
        verbose_name= _("Category"),
    )

    class Meta:
        verbose_name = _("Reference Limiting Factor")
        verbose_name_plural = _("Reference Limiting Factors")


class MaritalStatus(ReferenceLimitingFactor):
    is_active = models.BooleanField(
        default= False,
        verbose_name= _("is Active"),
    )

    class Meta:
        verbose_name = _("Marital Status")
        verbose_name_plural = _("Marital Status")


class Gender(ReferenceLimitingFactor):
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Gender")
        verbose_name_plural = _("Genders")


class AgeStage(ReferenceLimitingFactor): # المرحله العمريه

    class Meta:
        verbose_name = _("Age Stage")
        verbose_name_plural = _("Age Stages")


class MenstrualCycle(ReferenceLimitingFactor): # مراحل الدوره الشهريه

    class Meta:
        verbose_name = _("Menstrual Cycle")
        verbose_name_plural = _("Menstrual Cycles")


class SamplingTime(ReferenceLimitingFactor): # وقت سحب العينه
    
    class Meta:
        verbose_name = _("Sampling Time")
        verbose_name_plural = _("Sampling Times")


class SamplingEating(ReferenceLimitingFactor): # ارتباط سحب العينه بالاكل    
    
    class Meta:
        verbose_name = _("Correlation of sampling with eating")
        verbose_name_plural = _("Correlation of sampling with eatings")


class Person(Entity):

    national_id = models.CharField(
        max_length=14,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("National ID"),
    )
    family_name = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_("Family Name"),
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Birth Date"),
    )
    gender = models.ForeignKey(
        Gender,
        on_delete= models.SET("Deleted"),
        verbose_name= _("Gender"),
    )
    marital_status = models.ForeignKey(
        MaritalStatus,
        on_delete= models.SET("Deleted"),
        blank= True,
        null= True,
        verbose_name= _("Marital Status"),
    )  # الحاله الاجتماعيه
    Job = models.ForeignKey(
        Job,
        on_delete= models.SET("Deleted"),
        null= True,
        blank= True,
        verbose_name= _("Job"),
    )
    kinshipers = models.ManyToManyField(
        "self",
        through= "Kinship",
        verbose_name= _("Kinshipers"),
    )
    language = models.ForeignKey(
        Language,
        on_delete= models.SET("Deleted"),
        null= True,
        blank= True,
        default= "ar",
        related_name= -("Persons"),
        verbose_name= _("Language"),
    )    

    def get_full_name(self):
        return f"{self.name} {self.family_name}"
        
    @property
    def age(self):
        born = self.birth_date
        calendar.setfirstweekday(calendar.SUNDAY)
        today = date.today()
        if today.month >= born.month:
            year = today.year
        else:
            year = today.year - 1
        age_years = year - born.year
        try:  # raised when birth day is February 29 and the current year is not a leap year
            age_days = (today - (born.replace(year=year))).days
        except ValueError:
            age_days = (today - (born.replace(year=year, day=born.day - 1))).days + 1
        month = born.month
        age_months = 0
        while age_days > calendar.monthrange(year, month)[1]:
            age_days = age_days - calendar.monthrange(year, month)[1]
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
            age_months += 1
        return Age (
            year= age_years,
            month= age_months,
            day= age_days,
        )

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")


class Kinship(models.Model):
    # TODO Complete kinshipRelations Name
    class kinshipRelations(models.TextChoices):
        Father = _("Father")
        Mother = _("Mother")
        Brother = _("Brother")
        Sister = _("Sister")

    person = models.ForeignKey(
        Person,
        on_delete= models.CASCADE,
        verbose_name= _("Person"),
    )
    kinshiper = models.ForeignKey(
        Person,
        on_delete= models.CASCADE,
        related_name= _("kinshipers"),
        verbose_name= _("Kinshiper"),
    )
    relation = models.CharField(
        max_length= 20,
        choices= kinshipRelations.choices,
        verbose_name= _("Relation"),
    )

    @property
    def slug(self):
        return slugify(str(self.person))

    def __str__(self):
        return f"{self.person} -> {self.kinshiper}"

    class Meta:
        unique_together = (
            "person",
            "kinshiper",
        )
        verbose_name = _("Kinship")
        verbose_name_plural = _("Kinships")


class Employee(Person):

    work_in_branch = models.ForeignKey(
        Branch,
        on_delete= models.CASCADE,
        related_name= _("Employees"),
        verbose_name= _("Work in Branch"),
    )
    salary = models.FloatField(
        verbose_name= _("Salary"),
    )
    allowed_discount_rate = models.FloatField(
        default= 5.0,
        verbose_name= _("Allowed Discount Rate"),
    ) # نسبه الخصم المسموحه
    shifts = models.ManyToManyField(
        Shift,
        related_name= _("Employees"),
        verbose_name= _("Shifts"),
    )
        
    class Meta:
        permissions = [
            (
                "set_published_status",
                "Can set the status of the post to either publish or not"
            )
        ]
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")