# Generated by Django 3.2.16 on 2022-12-18 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Person', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Sample',
                'verbose_name_plural': 'Samples',
            },
        ),
        migrations.CreateModel(
            name='SamplingContainer',
            fields=[
                ('referencelimitingfactor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Person.referencelimitingfactor')),
            ],
            options={
                'verbose_name': 'Sampling Container',
                'verbose_name_plural': 'Sampling Containers',
            },
            bases=('Person.referencelimitingfactor',),
        ),
        migrations.CreateModel(
            name='SamplingTime',
            fields=[
                ('referencelimitingfactor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Person.referencelimitingfactor')),
                ('time', models.TimeField(verbose_name='Time')),
            ],
            options={
                'verbose_name': 'Sampling Time',
                'verbose_name_plural': 'Sampling Times',
            },
            bases=('Person.referencelimitingfactor',),
        ),
        migrations.CreateModel(
            name='Specimen',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Name')),
                ('comment', models.TextField(blank=True, max_length=200, null=True, verbose_name='Comment')),
                ('reference_limiting_factors', models.ManyToManyField(related_name='_Specimen_specimen_reference_limiting_factors_+', to='Person.ReferenceLimitingFactor', verbose_name='Reference Limiting Factors')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Specimens', to='Specimen.sample', verbose_name='Sample')),
            ],
            options={
                'verbose_name': 'Specimen',
                'verbose_name_plural': 'Specimens',
            },
        ),
    ]
