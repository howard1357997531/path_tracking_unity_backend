# Generated by Django 4.2.3 on 2023-08-08 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_rename_dotscol_object_3d_dotscol'),
    ]

    operations = [
        migrations.AddField(
            model_name='object_3d',
            name='is_pinned',
            field=models.BooleanField(default=False),
        ),
    ]
