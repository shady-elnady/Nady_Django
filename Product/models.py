from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from polymorphic.models import PolymorphicModel

from GraphQL.models import (
    BaseModelImage,
    BaseModelImageOnly,
    BaseModelName,
    FacilityTypes,
    Measurements,
)
from Unit.models import Unit
from Location.models import Address, Country
from Payment.models import Currency, Payment
from Facility.models import Facility
from Person.models import Person
from Employee.models import Employee


# Create your models here.


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


class Category(BaseModelName):
    category_parent= models.ForeignKey(
        "self",
        null= True,
        blank= True,
        limit_choices_to= {"category_parent__isnull": True},
        on_delete= models.CASCADE,
        related_name= _("Sub Categories+"),
        verbose_name= _("Category Parent"),
    )

    class Meta:
        verbose_name= _("Category")
        verbose_name_plural= _("Categories")


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
    serial = models.CharField(
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
    price = models.FloatField(
        blank=True,
        null=True,
        verbose_name= _("Price"),
    )
    discount_price = models.FloatField(
        default= 0,
        verbose_name= _("Discount Price"),
    )
    description = models.TextField(
        blank=True,
        null=True,
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



class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code
    
    @property
    def slug(self):
        return slugify(f"{self.code}")

    def __decode__(self):
        return f"{self.code}"
    
    class Meta:
        verbose_name= _("Coupon")
        verbose_name_plural= _("Coupons")


class Business(PolymorphicModel, models.Model):
    serial_no= models.CharField(
        max_length= 20,
        primary_key= True,
        verbose_name= _("Serial Number"),
    )
    products_items = models.ManyToManyField(
        ProductPackaging,
        through= "LineInInvoice",
        verbose_name= _("Products Items"),
    )
    created_at = models.DateTimeField(
        auto_now_add= True,
        verbose_name=_("Cearted At"),
    )
    received_date = models.DateTimeField(
        auto_now_add= True,
        editable= True,
        blank=True,
        verbose_name=_("Received Date"),
    ) # تاريخ الاستلام
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        blank= True,
        null= True,
        verbose_name= _("Coupon"),
    )
    is_received = models.BooleanField(
        default= False,
        verbose_name= _("is Received"),
    ) # تم الاستلام
    is_refund_requested = models.BooleanField(
        default= False,
        verbose_name= _("is Refund Requested"),
    ) # هو طلب استرداد
    is_refund_granted = models.BooleanField(
        default= False,
        verbose_name= _("is Refund Granted"),
    ) # تم رد الأموال الممنوحة
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        blank= True,
        null= True,
        related_name= _("Orders"),
        verbose_name= _("Payment"),
    )

    @property
    def final_price(self):
        total = 0
        for lineInInvoice in self.products_items.all():
            total += lineInInvoice.final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    class Meta:
        verbose_name= _("Business")
        verbose_name_plural= _("Business")


class BusinessPayment(Payment):
    business= models.ForeignKey(
        Business,
        on_delete= models.CASCADE,
        related_name= _("Payments"),
        verbose_name= _("Business"),
    )
    
    class Meta:
        verbose_name= _("Business Payment")
        verbose_name_plural= _("Business Payments")


class Invoice(Business):    
    employee = models.ForeignKey(
        Employee,
        on_delete= models.SET("Deleted"),
        related_name= _("Invoices"),
        verbose_name= _("Employee"),
    ) # موظف الاستقبال
    supplier = models.ForeignKey(
        Facility,
        limit_choices_to= {"supplier": FacilityTypes.Supplier},
        on_delete= models.SET("Deleted"),
        related_name= _("Invoices"),
        verbose_name= _("Supplier"),
    )

    class Meta:
        verbose_name= _("Invoice")
        verbose_name_plural= _("Invoices")
 

class LineInInvoice(models.Model):  #  Many to Many RealtionShip Product + Invoice
    invoice= models.ForeignKey(
        Business,
        on_delete= models.CASCADE,
        related_name= _("Lines_In_Invoices"),
        verbose_name= _("Invoice"),
    )
    product_item= models.ForeignKey(
        ProductPackaging,
        on_delete= models.CASCADE,
        related_name= _("Lines_In_Invoices"),
        verbose_name= _("Product Item"),
    )    
    expire_date= models.DateField(
        blank= True,
        null= True,
        verbose_name= _("Expire Date"),
    )    
    unit_packaging_quantity= models.FloatField(
        verbose_name= _("Unit Packaging Quantity"),
    )
    is_canceled = models.BooleanField(
        default= False,
        verbose_name= _("is Canceled"),
    )   # ملغى

    @property
    def total_price(self) -> float:
        return self.product_item.unit_packaging_price() * self.unit_packaging_quantity
    
    @property
    def total_discount_price(self) -> float:
        return self.unit_packaging_quantity * self.product_item.discount_price

    @property
    def final_price(self) -> float:
        if self.is_canceled :
            return 0.0
        return self.total_price()-self.total_discount_price()

    class Meta:
        unique_together = [
            [
                "invoice",
                "product_item",
            ]
        ]
        verbose_name= _("Line In Invoice")
        verbose_name_plural= _("Lines In Invoice")



################

'''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
'''

class Order(Business):
    customer = models.ForeignKey(
        Person,
        on_delete= models.CASCADE,
        verbose_name= _("Customer"),
    )
    shipping_address = models.ForeignKey(
        Address,
        related_name= 'shipping_address',
        on_delete= models.SET_NULL,
        blank= True,
        null= True,
        verbose_name= _("Shipping Address")
    ) # عنوان الشحن
    billing_address = models.ForeignKey(
        Address,
        related_name= 'billing_address',
        on_delete= models.SET_NULL,
        blank= True,
        null= True,
        verbose_name= _("Billing Address")
    ) # عنوان وصول الفواتير
    being_delivered = models.BooleanField(
        default=False,
    )
    # payment = models.ForeignKey(
    #     Payment,
    #     on_delete=models.CASCADE,
    #     blank= True,
    #     null= True,
    #     related_name= _("Orders"),
    #     verbose_name= _("Payment"),
    # )
    
    def __str__(self):
        return self.customer.name

    class Meta:
        verbose_name= _("Order")
        verbose_name_plural= _("Orders")


class Refund(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name= _("Refunds"),
        verbose_name= _("Order"),
    )
    reason = models.TextField(
        verbose_name= _("Reason"),
    )
    is_accepted = models.BooleanField(
        default=False,
        verbose_name= _("is Accepted"),
    )

    def __str__(self):
        return f"{self.pk}"
    
    class Meta:
        verbose_name= _("Refund")
        verbose_name_plural= _("Refunds")

