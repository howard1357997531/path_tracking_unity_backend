# Generated by Django 4.2.3 on 2023-12-28 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_initialobject_is_pined_alter_initialobject_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='initialobject',
            name='is_selected',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='initialobject',
            name='name',
            field=models.CharField(default='2023/12/28 14:41:22', max_length=255),
        ),
    ]