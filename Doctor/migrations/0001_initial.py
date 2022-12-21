# Generated by Django 3.2.16 on 2022-12-18 19:04

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Person', '0001_initial'),
        ('Facility', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Person.person')),
                ('nick_name', models.CharField(max_length=25, unique=True, verbose_name='Nick Name')),
                ('medical_specialty', models.CharField(choices=[('Ch', 'Childern')], max_length=4, verbose_name='Medical Specialty')),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctors',
            },
            bases=('Person.person',),
        ),
        migrations.CreateModel(
            name='PrivateClinic',
            fields=[
                ('facility_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Facility.facility')),
                ('owner_doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='private_clinics+', to='Doctor.doctor', verbose_name="Owner's Doctor")),
            ],
            options={
                'verbose_name': 'Private Clinic',
                'verbose_name_plural': 'Private Clinics',
            },
            bases=('Facility.facility',),
        ),
        migrations.AddField(
            model_name='doctor',
            name='private_clinics',
            field=djongo.models.fields.ArrayReferenceField(on_delete=djongo.models.fields.ArrayReferenceField._on_delete, to='Doctor.privateclinic'),
        ),
    ]