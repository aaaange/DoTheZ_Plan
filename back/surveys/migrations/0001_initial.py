# Generated by Django 4.2.16 on 2024-11-26 04:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSurvey',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deposit_or_saving', models.BooleanField()),
                ('minimum_deposit', models.FloatField()),
                ('investment_period', models.FloatField()),
                ('expected_return', models.FloatField()),
                ('interest_rate_type', models.CharField(choices=[('단리', '단리'), ('복리', '복리')], max_length=10)),
                ('investment_goal', models.CharField(choices=[('결혼자금', '결혼자금'), ('주택마련', '주택마련'), ('노후준비', '노후준비')], max_length=20)),
                ('spending_habit_1', models.CharField(choices=[('쇼핑', '쇼핑'), ('여가', '여가'), ('식비', '식비'), ('교통', '교통'), ('주거', '주거'), ('저축', '저축'), ('기타', '기타')], max_length=10)),
                ('spending_habit_2', models.CharField(choices=[('쇼핑', '쇼핑'), ('여가', '여가'), ('식비', '식비'), ('교통', '교통'), ('주거', '주거'), ('저축', '저축'), ('기타', '기타')], max_length=10)),
                ('spending_habit_3', models.CharField(choices=[('쇼핑', '쇼핑'), ('여가', '여가'), ('식비', '식비'), ('교통', '교통'), ('주거', '주거'), ('저축', '저축'), ('기타', '기타')], max_length=10)),
                ('fixed_income', models.FloatField()),
                ('main_bank', models.CharField(max_length=50)),
                ('household_type', models.CharField(choices=[('1인가구', '1인가구'), ('2인가구', '2인가구'), ('4인 이상', '4인 이상')], max_length=10)),
                ('age', models.IntegerField()),
                ('risk_tolerance', models.CharField(choices=[('낮음', '낮음'), ('보통', '보통'), ('높음', '높음')], max_length=20)),
                ('current_assets', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
