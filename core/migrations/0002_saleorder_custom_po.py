# Generated by Django 3.2 on 2022-04-04 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleorder',
            name='custom_po',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
