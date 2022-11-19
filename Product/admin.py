from django.contrib import admin

from .models import ProductItemImage, ProductPackaging

# # Register your models here.

 
class ProductItemImageAdmin(admin.StackedInline):
    model = ProductItemImage


@admin.register(ProductPackaging)
class ProductItemAdmin(admin.ModelAdmin):
    inlines = [ProductItemImageAdmin]
 
    class Meta:
       model = ProductPackaging


@admin.register(ProductItemImage)
class ProductItemImageAdmin(admin.ModelAdmin):
    pass
