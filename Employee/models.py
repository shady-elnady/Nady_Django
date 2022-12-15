from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from Facility.models import Branch, Shift
from Person.models import Person


# Create your models here.



# TODO Employee Attendance Management System
## https://itsourcecode.com/uml/employee-attendance-management-system-er-diagram-erd/


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


class Bonuss(models.Model): # المكافاءت
    employee= models.ForeignKey(
        Employee,
        on_delete= models.CASCADE,
        related_name= _("Bonusss"),    # TODO Add to Employee Mpdel
        verbose_name= _("Employee"),
    )
    _date= models.DateTimeField(
        default=now,
        verbose_name=_("Date"),
    )
    amount= models.FloatField(
        verbose_name= _("Amount"),
    )
    reason= models.TextField()

    class Meta:
        verbose_name = _("Bonuss")
        verbose_name_plural = _("Bonusss")


class Deduction(models.Model): # الخصومات
    employee= models.ForeignKey(
        Employee,
        on_delete= models.CASCADE,
        related_name= _("Deductions"),    # TODO Add to Employee Mpdel
        verbose_name= _("Employee"),
    )
    _date= models.DateTimeField(
        default=now,
        verbose_name=_("Date"),
    )
    amount= models.FloatField(
        verbose_name= _("Amount"),
    )
    reason= models.TextField()

    class Meta:
        verbose_name = _("Deduction")
        verbose_name_plural = _("Deductions")


class Vacation(models.Model): # الاجازات
    employee= models.ForeignKey(
        Employee,
        on_delete= models.CASCADE,
        related_name= _("Vacations"),    # TODO Add to Employee Mpdel
        verbose_name= _("Employee"),
    )
    _date= models.DateField(
        verbose_name=_("Date"),
    )
    shift= models.ForeignKey(
        Shift,
        on_delete= models.CASCADE,
        # related_name= _("Vacations"),
        verbose_name= _("Shift"),
    )
    is_accepted= models.BooleanField(
        default= True,
        verbose_name= _("is_Accepted"),
    )

    class Meta:
        verbose_name = _("Vacation")
        verbose_name_plural = _("Vacations")


class Attendance(models.Model):  # الحضور والغياب

    employee= models.ForeignKey(
        Employee,
        on_delete= models.CASCADE,
        related_name= _("Attendances"),    # TODO Add to Employee Mpdel
        verbose_name= _("Employee"),
    )
    attending_time= models.TimeField(
        verbose_name= _("Attending Time"),
    )  # الحضور
    leaving_time= models.TimeField(
        verbose_name= _("Leaving Time"),
    )  # الانصراف

    class Meta:
        verbose_name = _("Laboratory Attendance")
        verbose_name_plural = _("Laboratory Attendances")