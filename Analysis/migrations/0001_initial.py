# Generated by Django 3.2.16 on 2022-12-18 07:06

import GraphQL.models.methods
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Name')),
                ('symbol', models.CharField(max_length=10, unique=True, verbose_name='Symbol')),
                ('is_independent_report', models.BooleanField(default=False, verbose_name='is Independent Report')),
            ],
            options={
                'verbose_name': 'Analysis',
                'verbose_name_plural': 'Analysis',
            },
        ),
        migrations.CreateModel(
            name='AnalysisMethodExpectedResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=40, verbose_name='Value')),
                ('is_default_value', models.BooleanField(default=False, verbose_name='is Defaul Value')),
                ('is_Normal_value', models.BooleanField(default=False, verbose_name='is Normal Value')),
            ],
            options={
                'verbose_name': 'Analysis Method Expected Result',
                'verbose_name_plural': 'Analysis Method Expected Results',
            },
        ),
        migrations.CreateModel(
            name='EquationParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol_in_equation', models.CharField(max_length=1, verbose_name='Symbol in Equation')),
            ],
            options={
                'verbose_name': 'Equation Parameter',
                'verbose_name_plural': 'Equation Parameters',
            },
        ),
        migrations.CreateModel(
            name='Senstivity',
            fields=[
                ('name', models.CharField(choices=[('Strong', 'Strong'), ('Moderate', 'Mmderate'), ('Weak', 'Weak'), ('Very Weak', 'Very Weak')], max_length=10, primary_key=True, serialize=False, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Senstivity',
                'verbose_name_plural': 'Senstivites',
            },
        ),
        migrations.CreateModel(
            name='ShortCut',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'ShortCut',
                'verbose_name_plural': 'ShortCuts',
            },
        ),
        migrations.CreateModel(
            name='AnalysisMethod',
            fields=[
                ('analysis_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Analysis.analysis')),
                ('price_for_patient', models.FloatField(blank=True, null=True, verbose_name='Price For Patient')),
                ('price_for_laboratories', models.FloatField(blank=True, null=True, verbose_name='Price For Laboratories')),
                ('score', models.CharField(choices=[('A', '⭐'), ('B', '⭐⭐'), ('C', '⭐⭐⭐'), ('D', '⭐⭐⭐⭐'), ('E', '⭐⭐⭐⭐⭐'), ('F', '⭐⭐⭐⭐⭐⭐'), ('G', '⭐⭐⭐⭐⭐⭐⭐'), ('H', '⭐⭐⭐⭐⭐⭐⭐⭐'), ('I', '⭐⭐⭐⭐⭐⭐⭐⭐⭐'), ('J', '⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐'), ('K', '⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐'), ('L', '⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐'), ('M', '⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐'), ('N', '⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐'), ('O', '⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐')], max_length=1, verbose_name='Score')),
                ('is_default', models.BooleanField(default=True, verbose_name='is Default')),
            ],
            options={
                'verbose_name': 'Analysis Method',
                'verbose_name_plural': 'Analysis Methods',
            },
            bases=('Analysis.analysis',),
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('analysis_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Analysis.analysis')),
            ],
            options={
                'verbose_name': 'Function',
                'verbose_name_plural': 'Functions',
            },
            bases=('Analysis.analysis',),
        ),
        migrations.CreateModel(
            name='GroupAnalysis',
            fields=[
                ('analysis_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Analysis.analysis')),
            ],
            options={
                'verbose_name': 'Group Analysis',
                'verbose_name_plural': 'Group Analysis',
            },
            bases=('Analysis.analysis',),
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('analysis_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Analysis.analysis')),
            ],
            options={
                'verbose_name': 'Package',
                'verbose_name_plural': 'Packages',
            },
            bases=('Analysis.analysis',),
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('analysis_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Analysis.analysis')),
                ('is_constant', models.BooleanField(default=False, verbose_name='is Constant')),
            ],
            options={
                'verbose_name': 'Parameter',
                'verbose_name_plural': 'Parameters',
            },
            bases=('Analysis.analysis',),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('analysis_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Analysis.analysis')),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
            },
            bases=('Analysis.analysis',),
        ),
        migrations.CreateModel(
            name='ShortCutImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='images/{instance.__class__.__name__}/default.jpg', null=True, upload_to=GraphQL.models.methods.upload_to, verbose_name='Image')),
                ('shortCut', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ShortCut_Images', to='Analysis.shortcut', verbose_name='ShortCut')),
            ],
            options={
                'verbose_name': 'ShortCut Image',
                'verbose_name_plural': 'ShortCut Images',
            },
        ),
        migrations.CreateModel(
            name='AnalysisSpecimen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(choices=[('A', '⭐'), ('B', '⭐⭐'), ('C', '⭐⭐⭐'), ('D', '⭐⭐⭐⭐'), ('E', '⭐⭐⭐⭐⭐'), ('F', '⭐⭐⭐⭐⭐⭐'), ('G', '⭐⭐⭐⭐⭐⭐⭐'), ('H', '⭐⭐⭐⭐⭐⭐⭐⭐'), ('I', '⭐⭐⭐⭐⭐⭐⭐⭐⭐'), ('J', '⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐'), ('K', '⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐'), ('L', '⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐'), ('M', '⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐'), ('N', '⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐'), ('O', '⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐')], default='A', max_length=1, verbose_name='Score')),
                ('is_default', models.BooleanField(default=True, verbose_name='Is Default')),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Analysis.analysis', verbose_name='Analysis')),
            ],
            options={
                'verbose_name': 'Analysis Specimen',
                'verbose_name_plural': 'Analysis Specimens',
            },
        ),
    ]
