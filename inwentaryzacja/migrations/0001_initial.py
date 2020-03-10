# Generated by Django 3.0 on 2020-03-07 22:10

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Raport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_raportu', models.DateField(auto_now_add=True)),
                ('telefony_elza', models.IntegerField()),
                ('telefony_stan', models.IntegerField()),
                ('voice_elza', models.IntegerField()),
                ('voice_stan', models.IntegerField()),
                ('data_elza', models.IntegerField()),
                ('data_stan', models.IntegerField()),
                ('zdrapki_elza', models.IntegerField()),
                ('zdrapki_stan', models.IntegerField()),
                ('doladowania_elza', models.IntegerField()),
                ('doladowania_stan', models.IntegerField()),
                ('kasa_elza', models.DecimalField(decimal_places=2, max_digits=7)),
                ('kasa_stan', models.DecimalField(decimal_places=2, max_digits=7)),
                ('kto', models.ForeignKey(default=django.contrib.auth.models.User, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]