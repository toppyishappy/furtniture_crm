# Generated by Django 3.2 on 2022-03-14 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_saleorderdetail_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleorder',
            name='amphoe',
            field=models.CharField(default='e', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='saleorder',
            name='district',
            field=models.CharField(default='d', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='saleorder',
            name='province',
            field=models.CharField(default='d', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='saleorder',
            name='signature_id',
            field=models.IntegerField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='saleorder',
            name='zipcode',
            field=models.CharField(default='d', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='department',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='itemcolor',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='itemimage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='itemmaterial',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='itemmodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='saleorder',
            name='deposite_type',
            field=models.IntegerField(blank=True, choices=[(0, 'percentage'), (1, 'money')], null=True),
        ),
        migrations.AlterField(
            model_name='saleorder',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='saleorderdetail',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='worklocation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
