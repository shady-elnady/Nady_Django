# Generated by Django 3.2.16 on 2022-12-18 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Kat', '0002_initial'),
        ('Analysis', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysisbytechnique',
            name='kats',
            field=models.ManyToManyField(related_name='Analysis', to='Kat.Kat', verbose_name='Kats'),
        ),
        migrations.AddField(
            model_name='analysisbycalculatedmethod',
            name='equation_parameters',
            field=models.ManyToManyField(through='Analysis.EquationParameter', to='Analysis.Parameter', verbose_name='Equation Parameters'),
        ),
        migrations.AlterUniqueTogether(
            name='equationparameter',
            unique_together={('calculated_parameter', 'equation_parameter')},
        ),
    ]
