# Generated by Django 3.0.7 on 2021-07-14 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0049_auto_20210713_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.IntegerField(blank=True, choices=[(1, 'Наличностью'), (2, 'Электронно')], db_index=True, null=True, verbose_name='Способ оплаты'),
        ),
    ]