# Generated by Django 2.2.3 on 2019-09-03 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_auto_20190903_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pbguser',
            name='phone_number',
            field=models.CharField(default=0, max_length=50, null=True),
        ),
    ]
