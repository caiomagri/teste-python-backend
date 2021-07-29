# Generated by Django 3.2.5 on 2021-07-29 15:43

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lottery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='Usuário da Aposta'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bet',
            name='numbers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None, verbose_name='Números da Aposta'),
        ),
    ]
