# Generated by Django 3.2.16 on 2022-12-18 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Person', '0001_initial'),
        ('Unit', '0001_initial'),
        ('Employee', '0002_initial'),
        ('Specimen', '0001_initial'),
        ('Analysis', '0003_initial'),
        ('Prescription', '0001_initial'),
        ('Facility', '0003_publicfacility_owner'),
        ('Doctor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vitalsign',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Vital_Signs', to='Unit.unit', verbose_name='Unit'),
        ),
        migrations.AddField(
            model_name='prescriptionvitalsign',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Prescription.prescription', verbose_name='Prescription'),
        ),
        migrations.AddField(
            model_name='prescriptionvitalsign',
            name='vital_sign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Prescriptions', to='Prescription.vitalsign', verbose_name='Vital Sign'),
        ),
        migrations.AddField(
            model_name='prescriptionreportimage',
            name='prescription_report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Images', to='Prescription.prescriptionreport', verbose_name='Prescription Report'),
        ),
        migrations.AddField(
            model_name='prescriptionreport',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Reports', to='Prescription.prescription', verbose_name='Prescription'),
        ),
        migrations.AddField(
            model_name='prescriptionreport',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Analysis.report', verbose_name='Report'),
        ),
        migrations.AddField(
            model_name='prescriptionpayment',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Payments', to='Prescription.prescription', verbose_name='Prescription'),
        ),
        migrations.AddField(
            model_name='prescriptionemployeeactivity',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescription_prescriptionemployeeactivity_Visit', to='Prescription.prescription', verbose_name='Prescription'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Prescriptions', to='Facility.branch', verbose_name='Branch'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Prescriptions', to='Person.person', verbose_name='Patient'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='prescription_vital_Signs',
            field=models.ManyToManyField(through='Prescription.PrescriptionVitalSign', to='Prescription.VitalSign', verbose_name='Prescription Vital Signs'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='receptionist',
            field=models.ManyToManyField(through='Prescription.PrescriptionEmployeeActivity', to='Employee.Employee', verbose_name='Receptionist'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='transfer_destination',
            field=models.ForeignKey(blank=True, limit_choices_to={'facility_type': 'DA'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Prescriptions', to='Facility.facility', verbose_name='Transfer Destination'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='treating_doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Writed_Prescriptions', to='Doctor.doctor', verbose_name='Treating Doctor'),
        ),
        migrations.AddField(
            model_name='phlebotomyspecimen',
            name='phlebotomy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Prescription.phlebotomy', verbose_name='Phlebotomy'),
        ),
        migrations.AddField(
            model_name='phlebotomyspecimen',
            name='specimen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Specimen.specimen', verbose_name='Specimen'),
        ),
        migrations.AddField(
            model_name='phlebotomyemployeeactivity',
            name='phlebotomy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phlebotomists+', to='Prescription.phlebotomy', verbose_name='Phlebotomy'),
        ),
        migrations.AddField(
            model_name='phlebotomy',
            name='phlebotomists',
            field=models.ManyToManyField(through='Prescription.PhlebotomyEmployeeActivity', to='Employee.Employee', verbose_name='Phlebotomist'),
        ),
        migrations.AddField(
            model_name='phlebotomy',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Phlebotomy_Sessions', to='Prescription.prescription', verbose_name='Prescription'),
        ),
        migrations.AddField(
            model_name='phlebotomy',
            name='required_analysis',
            field=models.ManyToManyField(to='Analysis.AnalysisMethod', verbose_name='Required Analysis'),
        ),
        migrations.AddField(
            model_name='phlebotomy',
            name='specimens',
            field=models.ManyToManyField(related_name='Phlebotomys', through='Prescription.PhlebotomySpecimen', to='Specimen.Specimen', verbose_name='Specimens'),
        ),
        migrations.AddField(
            model_name='paymentemployeeactivity',
            name='phlebotomy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phlebotomists', to='Prescription.prescriptionpayment', verbose_name='Phlebotomy'),
        ),
        migrations.AddField(
            model_name='lineinreport',
            name='analysis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescription_lineinreport_Analysis', to='Analysis.analysismethod', verbose_name='Analysis'),
        ),
        migrations.AddField(
            model_name='lineinreport',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Analysis.groupanalysis', verbose_name='Group'),
        ),
        migrations.AddField(
            model_name='lineinreport',
            name='super_analysis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Sub_Analysis', to='Prescription.lineinreport', verbose_name='Super Analysis'),
        ),
        migrations.AlterUniqueTogether(
            name='prescriptionvitalsign',
            unique_together={('prescription', 'vital_sign')},
        ),
        migrations.AlterUniqueTogether(
            name='phlebotomyspecimen',
            unique_together={('phlebotomy', 'specimen')},
        ),
    ]
