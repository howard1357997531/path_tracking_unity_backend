# Generated by Django 4.2.3 on 2023-07-27 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_route'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='object_3d',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='route', to='mainapp.object_3d'),
        ),
    ]