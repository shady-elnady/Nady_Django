# Generated by Django 3.2.16 on 2022-12-18 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Invoice', '0001_initial'),
        ('Payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Payment.payment')),
            ],
            options={
                'verbose_name': 'Business Payment',
                'verbose_name_plural': 'Business Payments',
            },
            bases=('Payment.payment',),
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('amount', models.FloatField()),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
            },
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(verbose_name='Reason')),
                ('is_accepted', models.BooleanField(default=False, verbose_name='is Accepted')),
            ],
            options={
                'verbose_name': 'Refund',
                'verbose_name_plural': 'Refunds',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('business_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Invoice.business')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
            bases=('Invoice.business',),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('business_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Invoice.business')),
                ('being_delivered', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
            bases=('Invoice.business',),
        ),
        migrations.CreateModel(
            name='LineInInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expire_date', models.DateField(blank=True, null=True, verbose_name='Expire Date')),
                ('unit_packaging_quantity', models.FloatField(verbose_name='Unit Packaging Quantity')),
                ('is_canceled', models.BooleanField(default=False, verbose_name='is Canceled')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Lines_In_Invoices', to='Invoice.business', verbose_name='Invoice')),
            ],
            options={
                'verbose_name': 'Line In Invoice',
                'verbose_name_plural': 'Lines In Invoice',
            },
        ),
    ]