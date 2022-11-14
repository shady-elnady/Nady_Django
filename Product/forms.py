from django import forms

from .models import ProductItem, ProductItemImage


class ProductItemForm(forms.ModelForm):

    class Meta:
        model= ProductItem
        fields= '__all__'


class ProductImageForm(forms.ModelForm):
    image= forms.ImageField(
        label= "Image",
        widget= forms.ClearableFileInput(attrs={"multiple": True}),
    )

    class Meta:
        model= ProductItemImage
        fields= ("image")