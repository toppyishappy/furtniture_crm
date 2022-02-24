# Generated by Django 3.2 on 2022-02-23 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleOrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_id', models.IntegerField()),
                ('color_id', models.IntegerField()),
                ('material_id', models.IntegerField()),
                ('type_id', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='itemimage',
            name='order',
        ),
        migrations.RemoveField(
            model_name='saleorder',
            name='color_id',
        ),
        migrations.RemoveField(
            model_name='saleorder',
            name='material_id',
        ),
        migrations.RemoveField(
            model_name='saleorder',
            name='model_id',
        ),
        migrations.RemoveField(
            model_name='saleorder',
            name='type_id',
        ),
        migrations.AddField(
            model_name='saleorder',
            name='deposite_money',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='saleorder',
            name='deposite_type',
            field=models.CharField(default=0, max_length=5),
        ),
        migrations.AlterField(
            model_name='saleorder',
            name='payment_method',
            field=models.IntegerField(blank=True, choices=[(0, 'cash'), (1, 'credit')], null=True),
        ),
        migrations.AlterField(
            model_name='saleorder',
            name='status',
            field=models.IntegerField(choices=[(0, 'percetange'), (1, 'money')], default=0),
        ),
        migrations.AlterField(
            model_name='saleorder',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='itemimage',
            name='order_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.saleorderdetail'),
        ),
    ]
