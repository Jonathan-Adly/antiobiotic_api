# Generated by Django 4.0.8 on 2022-11-16 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_drug_renal_comments_delete_renaldose'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indication',
            name='similar_terms',
        ),
        migrations.RemoveField(
            model_name='indication',
            name='virus',
        ),
        migrations.AlterField(
            model_name='formulation',
            name='value',
            field=models.IntegerField(help_text='amount of milligrams/units per mL for non-pill, or amount of milligrams per pill'),
        ),
    ]
