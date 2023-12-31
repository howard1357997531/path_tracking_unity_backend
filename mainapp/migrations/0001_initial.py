# Generated by Django 4.2.3 on 2023-07-27 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='object_3d',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('date', models.CharField(blank=True, max_length=225, null=True)),
                ('dotscol', models.CharField(blank=True, max_length=225, null=True)),
                ('image', models.TextField(blank=True, null=True)),
                ('modelCol', models.CharField(blank=True, max_length=225, null=True)),
                ('name', models.CharField(blank=True, max_length=225, null=True)),
                ('rotation', models.CharField(blank=True, max_length=225, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
