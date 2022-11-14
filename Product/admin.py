from django.contrib import admin

from .models import ProductItem, ProductItemImage

# # Register your models here.

 
class ProductItemImageAdmin(admin.StackedInline):
    model = ProductItemImage


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    inlines = [ProductItemImageAdmin]
 
    class Meta:
       model = ProductItem


@admin.register(ProductItemImage)
class ProductItemImageAdmin(admin.ModelAdmin):
    pass
