# Generated by Django 3.2.16 on 2022-12-18 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Analysis', '0001_initial'),
        ('Specimen', '0001_initial'),
        ('Person', '0001_initial'),
        ('Facility', '0003_publicfacility_owner'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('Kat', '0001_initial'),
        ('Analytic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysisspecimen',
            name='specimen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Analysis', to='Specimen.specimen', verbose_name='Specimen'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_analysis.analysis_set+', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='shortCuts',
            field=models.ManyToManyField(to='Analysis.ShortCut', verbose_name='ShortCuts'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='specimens',
            field=models.ManyToManyField(through='Analysis.AnalysisSpecimen', to='Specimen.Specimen', verbose_name='Specimens'),
        ),
        migrations.CreateModel(
            name='AnalysisByCalculatedMethod',
            fields=[
                ('analysismethod_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Analysis.analysismethod')),
                ('equation', models.CharField(max_length=25, verbose_name='Equation')),
            ],
            options={
                'verbose_name': 'Analysis By Calculated Method',
                'verbose_name_plural': 'Analysis By Calculated Methods',
            },
            bases=('Analysis.analysismethod',),
        ),
        migrations.CreateModel(
            name='AnalysisByTechnique',
            fields=[
                ('analysismethod_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Analysis.analysismethod')),
                ('run_time', models.CharField(choices=[('SD', 'Same Day'), ('ND', 'Next Day'), ('2D', 'After 2Days'), ('4D', 'After 4Days'), ('10D', 'After 10Days'), ('AW', 'After Week'), ('AM', 'After Month'), ('Sat', 'Monday'), ('Sun', 'Tuesday'), ('Mon', 'Wednesday'), ('Tue', 'Thursday'), ('Wed', 'Friday'), ('Thu', 'Saturday'), ('Fri', 'Sunday')], max_length=4, verbose_name='Run Time')),
                ('is_available', models.BooleanField(default=True, verbose_name='is Available')),
            ],
            options={
                'verbose_name': 'Analysis By Technique',
                'verbose_name_plural': 'Analysis By Techniques',
            },
            bases=('Analysis.analysismethod',),
        ),
        migrations.AddField(
            model_name='parameter',
            name='analytics',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Parameters', to='Analytic.analytics', verbose_name='Analytics'),
        ),
        migrations.AddField(
            model_name='parameter',
            name='belong_to_function',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Parameters_in_Function', to='Analysis.function', verbose_name='Function'),
        ),
        migrations.AddField(
            model_name='parameter',
            name='belong_to_report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Parameters_in_Report', to='Analysis.report', verbose_name='Report'),
        ),
        migrations.AddField(
            model_name='parameter',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Parameters_in_Group', to='Analysis.groupanalysis', verbose_name='Group'),
        ),
        migrations.AddField(
            model_name='parameter',
            name='reference_limiting_factors',
            field=models.ManyToManyField(related_name='_Analysis_parameter_reference_limiting_factors_+', to='Person.ReferenceLimitingFactor', verbose_name='Reference Limiting Factors'),
        ),
        migrations.AddField(
            model_name='parameter',
            name='sample',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Parameters', to='Specimen.sample', verbose_name='Sample'),
        ),
        migrations.AddField(
            model_name='parameter',
            name='sub_analysis',
            field=models.ManyToManyField(related_name='_Analysis_parameter_sub_analysis_+', to='Analysis.Parameter', verbose_name='Sub Analysis'),
        ),
        migrations.AddField(
            model_name='package',
            name='analysis_in_package',
            field=models.ManyToManyField(related_name='Package', to='Analysis.Analysis', verbose_name='Analysis in Package'),
        ),
        migrations.AddField(
            model_name='groupanalysis',
            name='belong_to_function',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Analysis_in_Function', to='Analysis.function', verbose_name='Function'),
        ),
        migrations.AddField(
            model_name='equationparameter',
            name='equation_parameter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equation_parameters', to='Analysis.parameter', verbose_name='Equation Parameter'),
        ),
        migrations.AlterUniqueTogether(
            name='analysisspecimen',
            unique_together={('analysis', 'specimen')},
        ),
        migrations.AddField(
            model_name='analysismethodexpectedresult',
            name='analysis_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Analysis_Method_Expected_Values', to='Analysis.analysismethod', verbose_name='AnalysisMethod'),
        ),
        migrations.AddField(
            model_name='analysismethod',
            name='analysis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Analysis', to='Analysis.analysis', verbose_name='Analysis'),
        ),
        migrations.AddField(
            model_name='analysismethod',
            name='analytical_technique',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Analysis', to='Kat.analyticaltechnique', verbose_name='Analytical Technique'),
        ),
        migrations.AddField(
            model_name='analysismethod',
            name='departement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Analysis', to='Facility.departement', verbose_name='Departement'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='analysis_methods',
            field=models.ManyToManyField(through='Analysis.AnalysisMethod', to='Kat.AnalyticalTechnique', verbose_name='Analysis Methods'),
        ),
        migrations.CreateModel(
            name='Lab2LabMenu',
            fields=[
                ('analysismethod_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Analysis.analysismethod')),
                ('run_time', models.CharField(choices=[('SD', 'Same Day'), ('ND', 'Next Day'), ('2D', 'After 2Days'), ('4D', 'After 4Days'), ('10D', 'After 10Days'), ('AW', 'After Week'), ('AM', 'After Month'), ('Sat', 'Monday'), ('Sun', 'Tuesday'), ('Mon', 'Wednesday'), ('Tue', 'Thursday'), ('Wed', 'Friday'), ('Thu', 'Saturday'), ('Fri', 'Sunday')], max_length=4, verbose_name='Run Time')),
                ('cost', models.FloatField(blank=True, null=True, verbose_name='Cost')),
                ('laboratory', models.ForeignKey(limit_choices_to={'facility_type': 'ML'}, on_delete=django.db.models.deletion.CASCADE, related_name='Analysis', to='Facility.facility', verbose_name='Laboratory')),
                ('reference_range', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Kat_Samples+', to='Analytic.referencerange', verbose_name='Reference Range')),
            ],
            options={
                'verbose_name': 'Lab2Lab Menu',
                'verbose_name_plural': 'Lab2Lab Menus',
            },
            bases=('Analysis.analysismethod',),
        ),
        migrations.AddField(
            model_name='equationparameter',
            name='calculated_parameter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Analysis.analysisbycalculatedmethod', verbose_name='Calculated Parameter'),
        ),
    ]