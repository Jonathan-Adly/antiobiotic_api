# Generated by Django 4.0.8 on 2022-11-09 16:41

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('drug_name', models.CharField(max_length=100)),
                ('brand_name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('is_sulfa', models.BooleanField(default=False)),
                ('is_penicillin', models.BooleanField(default=False)),
                ('is_cephalosporin', models.BooleanField(default=False)),
                ('similar_terms', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('is_combo', models.BooleanField(default=False)),
                ('hepatic_adjustment', models.BooleanField(default=False)),
                ('hepatic_comments', models.TextField(blank=True)),
                ('renal_adjustment', models.BooleanField(default=False)),
                ('is_generic', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Indication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField()),
                ('disease_system', models.CharField(max_length=150)),
                ('similar_terms', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('comments', models.TextField(blank=True)),
                ('virus', models.BooleanField(default=False)),
                ('drug', models.ManyToManyField(related_name='indications', to='api.drug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RenalDose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('crcl_min', models.IntegerField()),
                ('crcl_max', models.IntegerField()),
                ('route', models.CharField(choices=[('po', 'Oral'), ('iv', 'IV'), ('sl', 'Sublingual'), ('pr', 'rectal'), ('im', 'IM'), ('sc', 'SC'), ('n', 'Intranasal'), ('in', 'Inhaled'), ('pv', 'Vaginal')], max_length=2)),
                ('weight_based_per_dose', models.IntegerField()),
                ('weight_based_freq', models.IntegerField(help_text='per day')),
                ('weight_based_dosing_unit', models.CharField(max_length=50)),
                ('duration', models.IntegerField()),
                ('duration_unit', models.CharField(max_length=20)),
                ('adult_per_dose', models.IntegerField()),
                ('adult_freq', models.IntegerField()),
                ('adult_dose_unit', models.CharField(max_length=20)),
                ('indication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renal_dosages', to='api.indication')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Formulation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('route', models.CharField(choices=[('po', 'Oral'), ('iv', 'IV'), ('sl', 'Sublingual'), ('pr', 'rectal'), ('im', 'IM'), ('sc', 'SC'), ('n', 'Intranasal'), ('in', 'Inhaled'), ('pv', 'Vaginal')], max_length=2)),
                ('label', models.CharField(max_length=250)),
                ('dosage_form', models.CharField(choices=[('suspension/liquid', 'Liquid/Powder for Suspension'), ('tablet', 'Tablet'), ('capsule', 'Capsule'), ('chewable', 'Chewable'), ('suppository', 'Suppository'), ('iv', 'IV'), ('sl', 'Sublingual'), ('im', 'IM'), ('sc', 'SC'), ('n', 'Intranasal'), ('in', 'Inhaled'), ('pv', 'Vaginal')], max_length=20)),
                ('is_pill', models.BooleanField()),
                ('value', models.IntegerField(help_text='amount of milligrams per mL for non-pill, or amount of milligrams per pill')),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formulations', to='api.drug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dosage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('route', models.CharField(choices=[('po', 'Oral'), ('iv', 'IV'), ('sl', 'Sublingual'), ('pr', 'rectal'), ('im', 'IM'), ('sc', 'SC'), ('n', 'Intranasal'), ('in', 'Inhaled'), ('pv', 'Vaginal')], max_length=2)),
                ('weight_based_per_dose', models.IntegerField()),
                ('weight_based_freq', models.IntegerField(help_text='per day')),
                ('weight_based_dosing_unit', models.CharField(max_length=50)),
                ('duration', models.IntegerField()),
                ('duration_unit', models.CharField(max_length=20)),
                ('adult_per_dose', models.IntegerField()),
                ('adult_freq', models.IntegerField()),
                ('adult_dose_unit', models.CharField(max_length=20)),
                ('indication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dosages', to='api.indication')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bacteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=250)),
                ('group', models.CharField(choices=[('gram+', 'gram-positive'), ('gram-', 'gram-negative'), ('anaerobic', 'anaerobic')], max_length=10)),
                ('possible_drugs', models.ManyToManyField(related_name='bacteria', to='api.drug')),
                ('possible_indications', models.ManyToManyField(related_name='bacteria', to='api.indication')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
