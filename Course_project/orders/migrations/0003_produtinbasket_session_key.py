# Generated by Django 3.0.4 on 2020-05-09 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200509_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='produtinbasket',
            name='session_key',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
    ]