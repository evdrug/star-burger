# Generated by Django 3.0.7 on 2020-10-29 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0040_auto_20201029_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.IntegerField(choices=[(1, 'Наличностью'), (2, 'Электронно')], default=1, verbose_name='Способ оплаты'),
        ),
    ]
