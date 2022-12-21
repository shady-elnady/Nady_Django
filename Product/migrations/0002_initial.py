# Generated by Django 3.2.16 on 2022-12-18 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Product', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('Unit', '0001_initial'),
        ('Facility', '0003_publicfacility_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpackaging',
            name='unit_packaging',
            field=models.ForeignKey(limit_choices_to={'measurement__equal': 'P'}, on_delete=django.db.models.deletion.CASCADE, to='Unit.unit', verbose_name='Unit Packaging'),
        ),
        migrations.AddField(
            model_name='productitemimage',
            name='product_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Images', to='Product.productpackaging', verbose_name='Product Item'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Products', to='Facility.brand', verbose_name='Brand'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(limit_choices_to={'category_parent__isnull': False}, on_delete=django.db.models.deletion.CASCADE, related_name='Products', to='Unit.category', verbose_name='Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='measurment_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Measurment_Products', to='Unit.unit', verbose_name='Measurment Unit'),
        ),
        migrations.AddField(
            model_name='product',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_product.product_set+', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_packaging_items',
            field=models.ManyToManyField(through='Product.ProductPackaging', to='Unit.Unit', verbose_name='Product Packaging Items'),
        ),
        migrations.AlterUniqueTogether(
            name='productpackaging',
            unique_together={('product_item', 'unit_packaging', 'volume')},
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('name', 'brand')},
        ),
    ]