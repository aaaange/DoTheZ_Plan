# Generated by Django 4.2.16 on 2024-11-21 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('fin_prdt_cd', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('is_saving', models.BooleanField()),
                ('fin_co_no', models.CharField(max_length=255)),
                ('fin_prdt_nm', models.CharField(default='Unknown', max_length=255)),
                ('join_way', models.CharField(max_length=255)),
                ('mtrt_int', models.TextField()),
                ('spcl_cnd', models.TextField()),
                ('join_deny', models.CharField(max_length=255, null=True)),
                ('etc_note', models.TextField(default='')),
                ('max_limit', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.TextField()),
                ('is_saving', models.BooleanField()),
                ('intr_rate_type_nm', models.CharField(max_length=255)),
                ('rsrv_type_nm', models.CharField(max_length=255, null=True)),
                ('save_trm', models.IntegerField()),
                ('intr_rate', models.FloatField()),
                ('intr_rate2', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
