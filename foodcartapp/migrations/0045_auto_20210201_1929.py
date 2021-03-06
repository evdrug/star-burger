# Generated by Django 3.0.7 on 2021-02-01 16:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_auto_20210127_1458'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderelements',
            options={'verbose_name': 'продукт в заказе', 'verbose_name_plural': 'продукты в заказе'},
        ),
        migrations.AlterField(
            model_name='order',
            name='called_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Время подтверждения заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Время поступления заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivered_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Время доставки заказа'),
        ),
        migrations.AlterField(
            model_name='orderelements',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_product', to='foodcartapp.Order', verbose_name='заказ'),
        ),
        migrations.AlterField(
            model_name='orderelements',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_product', to='foodcartapp.Product', verbose_name='товар'),
        ),
    ]
