from django.db import models
from django.utils.translation import gettext_lazy as _

from polymorphic.models import PolymorphicModel

from GraphQL.models import BaseModel, BaseModelImage
# Create your models here.



class Entity(PolymorphicModel, BaseModelImage, BaseModel):

    public_communication_ways = models.ManyToManyField(
        "Location.CommunicationWay",
        related_name= _("Public_Communication_Way"),
        verbose_name= _("Public Communication Ways"),
    )  # طرق الاتصال

    class Meta:
        verbose_name = _("Entity")
        verbose_name_plural = _("Entities")