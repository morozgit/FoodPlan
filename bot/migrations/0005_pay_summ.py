# Generated by Django 4.2.5 on 2023-09-29 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_alter_receptitem_unit_pay'),
    ]

    operations = [
        migrations.AddField(
            model_name='pay',
            name='summ',
            field=models.FloatField(default=100),
        ),
    ]
