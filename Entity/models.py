from django.db import models
from django.utils.translation import gettext_lazy as _

from polymorphic.models import PolymorphicModel

from GraphQL.models import BaseModelImage
from Location.models import CommunicationWay

# Create your models here.


class Entity(PolymorphicModel, BaseModelImage):

    communication_ways= models.ManyToManyField(
        CommunicationWay,
        through= "EntityCommunicationWay",
        verbose_name= _("Communication Ways"),
    )  # طرق الاتصال
    created_date= models.DateTimeField(
        auto_now_add= True,
        editable= False,
        verbose_name= _("Created Date"),
    )

    class Meta:
        verbose_name= _("Entity")
        verbose_name_plural= _("Entities")


class EntityCommunicationWay(models.Model):
    entity= models.ForeignKey(
        Entity,
        on_delete= models.CASCADE,
        verbose_name= _("Entity"),
    )
    communication_way= models.ForeignKey(
        CommunicationWay,
        on_delete= models.CASCADE,
        related_name= _("Entities"),
        verbose_name= _("Communication Way"),
    )
    is_owner= models.BooleanField(
        default= True,
        verbose_name= _("is Owner"),
    )

    class Meta:
        unique_together= [
            [
                "entity",
                "communication_way",
            ]
        ]
        verbose_name= _("Entity CommunicationWay")
        verbose_name_plural= _("Entity CommunicationWays")