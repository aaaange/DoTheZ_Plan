# Generated by Django 4.2.16 on 2024-11-26 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userproduct',
            name='productoption',
        ),
    ]
