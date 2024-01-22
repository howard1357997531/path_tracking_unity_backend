# Generated by Django 4.2.3 on 2024-01-22 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0019_drawobject_order_alter_initialobject_name_ovalpoint'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drawobject',
            name='order',
        ),
        migrations.AlterField(
            model_name='initialobject',
            name='name',
            field=models.CharField(default='2024/01/22 16:37:53', max_length=255),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('index', models.CharField(blank=True, max_length=225, null=True)),
                ('draw_object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='mainapp.drawobject')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]