# Generated by Django 3.2.16 on 2022-12-18 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Name')),
                ('native', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Native')),
                ('iso_639_1', models.CharField(max_length=5, unique=True, verbose_name='ISO_639_1')),
                ('is_rtl', models.BooleanField(default=False, verbose_name='is RightToLeft')),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
        ),
    ]
