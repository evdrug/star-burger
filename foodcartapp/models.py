from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField('название', max_length=50)
    address = models.CharField('адрес', max_length=100, blank=True)
    contact_phone = models.CharField('контактный телефон', max_length=50,
                                     blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'


class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.distinct().filter(menu_items__availability=True)


class ProductCategory(models.Model):
    name = models.CharField('название', max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('название', max_length=50)

    category = models.ForeignKey(ProductCategory, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name='категория',
                                 related_name='products')
    price = models.DecimalField('цена', max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(0)])
    image = models.ImageField('картинка')
    special_status = models.BooleanField('спец.предложение', default=False,
                                         db_index=True)
    description = models.TextField('описание', max_length=200, blank=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   related_name='menu_items',
                                   verbose_name="ресторан")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='menu_items',
                                verbose_name='продукт')
    availability = models.BooleanField('в продаже', default=True,
                                       db_index=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]


class Order(models.Model):
    STATUS_ORDER = (
        (1, 'Необработанный'),
        (2, 'Готовится'),
        (3, 'Выполнен'),
    )
    PAYMENT_ORDER = (
        (1, 'Наличностью'),
        (2, 'Электронно'),
    )
    address = models.CharField('Адрес', max_length=100)
    firstname = models.CharField('Имя', max_length=50)
    lastname = models.CharField('Фамилия', max_length=50)
    phonenumber = models.CharField('Мобильный номер', max_length=20)
    status = models.IntegerField('Статус заказа', choices=STATUS_ORDER,
                                 default=1)
    payment_method = models.IntegerField('Способ оплаты',
                                         choices=PAYMENT_ORDER,
                                         default=1)
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Время поступления заказа',
                                      default=timezone.now)
    called_at = models.DateTimeField('Время подтверждения заказа', blank=True,
                                     null=True)
    delivered_at = models.DateTimeField('Время доставки заказа', blank=True,
                                        null=True)

    def __str__(self):
        return "{} {} {}".format(self.firstname, self.lastname, self.address)

    class Meta:
        verbose_name = 'заках'
        verbose_name_plural = 'заказы'


class OrderElements(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='товар')
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              verbose_name='заказ', related_name='products')
    count = models.IntegerField(validators=[MinValueValidator(1)],
                                verbose_name='количество')
    price = models.DecimalField('цена за еденицу товара', max_digits=8,
                                decimal_places=2)

    def save(self, *args, **kwargs):
        self.price = float(self.product.price) * int(self.count)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'

    def __str__(self):
        return f"{self.product.name} {self.order}"
