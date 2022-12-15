from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from polymorphic.models import PolymorphicModel

from GraphQL.models import (
    BaseModelImageOnly,
    Measurements,
)
from Unit.models import Category, Unit
from Payment.models import Currency
from Facility.models import Brand

# Create your models here.


class Product(PolymorphicModel):  # Weak Entity
    name= models.CharField(
        max_length=100,
        verbose_name=_("Name"),
    )
    brand= models.ForeignKey(
        Brand,
        on_delete= models.CASCADE,
        related_name= _("Products"),
        verbose_name= _("Brand"),
    )
    category= models.ForeignKey(
        Category,
        limit_choices_to= {"category_parent__isnull": False},
        on_delete= models.CASCADE,
        related_name= _("Products"),
        verbose_name= _("Category"),
    )
    product_packaging_items= models.ManyToManyField(
        Unit,
        through= "ProductPackaging",
        verbose_name= _("Product Packaging Items"),
    )
    measurment_unit= models.ForeignKey(
        Unit,
        on_delete= models.CASCADE,
        related_name= _("Measurment_Products"),
        verbose_name= _("Measurment Unit"),
    )

    @property
    def slug(self) -> str:
        return slugify(f"{self.name}-{self.brand}")

    def __str__(self) -> str:
        return f"{self.name}-{self.brand}"

    def __decode__(self) -> str:
        return f"{self.name}-{self.brand}"
    
    # def get_absolute_url(self):
    #     return reverse("Vegetable:vegetable_detail", args=[self.slug])

    class Meta:
        unique_together = (
            "name",
            "brand",
        )
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class ProductPackaging(models.Model):
    product_item= models.ForeignKey(
        Product,
        on_delete= models.CASCADE,
        verbose_name= _("Product Item"),
    )
    unit_packaging = models.ForeignKey(
        Unit,
        limit_choices_to= {"measurement__equal": Measurements.Package},
        on_delete= models.CASCADE,
        verbose_name= _("Unit Packaging"),
    ) # العبوه الرئيسيه
    volume= models.FloatField(
        verbose_name= _("Volume"),
    )
    serial= models.CharField(
        max_length= 50,
        unique= True,
        verbose_name= _("Serial No."),
    )
    currency= models.ForeignKey(
        Currency,
        default= settings.DEFAULT_CURRENCY,
        on_delete= models.CASCADE,
        related_name= _("Invoices"),
        verbose_name= _("Currency"),
    )
    price= models.FloatField(
        blank=True,
        null=True,
        verbose_name= _("Price"),
    )
    discount_price= models.FloatField(
        default= 0,
        verbose_name= _("Discount Price"),
    )
    description= models.TextField(
        blank= True,
        null= True,
        verbose_name= _("Discrption"),
    )

    @property
    def name(self) -> str:
        return f"{self.product_item.name}-{self.volume}-{self.unit_packaging.name}"
    
    @property
    def unit_packaging_price(self) -> float:
        return self.price-self.discount_price
    
    @property
    def slug(self) -> str:
        return slugify(f"{self.name()}")

    def __str__(self) -> str:
        return f"{self.name()}"

    def __decode__(self) -> str:
        return f"{self.name()}"
    
    # def get_absolute_url(self):
    #     return reverse("Vegetable:vegetable_detail", args=[self.slug])

    class Meta:
        unique_together = (
            "product_item",
            "unit_packaging",
            "volume",
        )
        verbose_name= _("ProductPackaging")
        verbose_name_plural= _("ProductPackaging")


class ProductItemImage(BaseModelImageOnly):
    product_item = models.ForeignKey(
        ProductPackaging,
        on_delete= models.CASCADE,
        related_name= _("Images"),
        verbose_name= _("Product Item"),
    )

    @property
    def name(self) -> str:
        return f"{self.product_item.name}_{self.pk}"
    
    @property
    def slug(self) -> str:
        return slugify(f"{self.name}")

    def __str__(self) -> str:
        return f"{self.name}"

    def __decode__(self) -> str:
        return f"{self.name}"
    
    # def get_absolute_url(self):
    #     return reverse("Vegetable:vegetable_detail", args=[self.slug])

    class Meta:
        verbose_name= _("Product Image")
        verbose_name_plural= _("Product Images")