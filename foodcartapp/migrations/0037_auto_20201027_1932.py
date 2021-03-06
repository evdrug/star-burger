# Generated by Django 3.0.7 on 2020-10-27 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0036_order_orderelements'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderelements',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='цена за еденицу товара'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderelements',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='foodcartapp.Order', verbose_name='заказ'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_category', to='foodcartapp.ProductCategory', verbose_name='категория'),
        ),
    ]
