# Generated by Django 3.2.16 on 2022-12-18 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Analytic', '0002_initial'),
        ('Unit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referencerange',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Reference_Ranges', to='Unit.unit', verbose_name='Unit'),
        ),
        migrations.AddField(
            model_name='analyticsunitconvert',
            name='analytics_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Analytic.analyticsunit', verbose_name='Analytics'),
        ),
        migrations.AddField(
            model_name='analyticsunitconvert',
            name='to_analytics_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Convert_To_Units', to='Analytic.analyticsunit', verbose_name='Unit'),
        ),
        migrations.AddField(
            model_name='analyticsunit',
            name='analytics',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Analytic.analytics', verbose_name='Analytics'),
        ),
        migrations.AddField(
            model_name='analyticsunit',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Unit.unit', verbose_name='Unit'),
        ),
        migrations.AddField(
            model_name='analytics',
            name='units',
            field=models.ManyToManyField(through='Analytic.AnalyticsUnit', to='Unit.Unit', verbose_name='Units'),
        ),
        migrations.AlterUniqueTogether(
            name='analyticsunitconvert',
            unique_together={('analytics_unit', 'to_analytics_unit')},
        ),
        migrations.AlterUniqueTogether(
            name='analyticsunit',
            unique_together={('analytics', 'unit')},
        ),
    ]