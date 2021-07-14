# Generated by Django 3.0.7 on 2021-07-13 16:29

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0045_auto_20210201_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.IntegerField(choices=[(1, 'Наличностью'), (2, 'Электронно')], db_index=True, default=1, verbose_name='Способ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=20, region='RU', verbose_name='Мобильный номер'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Необработанный'), (2, 'Готовится'), (3, 'Выполнен')], db_index=True, default=1, verbose_name='Статус заказа'),
        ),
    ]