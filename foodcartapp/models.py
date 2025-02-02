from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Count, F, Sum
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class OrderQueryset(models.QuerySet):
    def get_order(self):
        return self.annotate(
            order_price=Sum(F('order_items__product__price') * F('order_items__quantity'))
        )


class RestaurantMenuItemQueryset(models.QuerySet):
    def get_restaurants(self, products):
        return self.filter(product__id__in=products) \
            .values('restaurant__name', 'restaurant__address')\
            .annotate(count_items=(Count('product__id'))).filter(count_items=len(products))


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )
    objects = RestaurantMenuItemQueryset.as_manager()

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    ORDER_STATE_CHOICES = [
        ('accepted', 'Обрабатывается'),
        ('packing', 'Упаковывается'),
        ('delivery', 'Передан в доставку'),
        ('done', 'Выполнен')
    ]
    PAYMENT_CHOICES = [
        ('specify', 'Выяснить'),
        ('cash', 'Наличные'),
        ('card', 'Карта')
    ]
    address = models.CharField(
        'адрес',
        max_length=100,
        db_index=True,
    )
    firstname = models.CharField(
        'имя',
        max_length=50,
        db_index=True,
    )
    lastname = models.CharField(
        'фамилия',
        max_length=50,
        db_index=True,
    )
    phonenumber = PhoneNumberField(
        'телефон',
        db_index=True,
    )
    status = models.CharField(
        'Статус',
        max_length=50,
        choices=ORDER_STATE_CHOICES,
        default='Обрабатывается',
        db_index=True
    )
    comment = models.TextField('Комментарий к заказу', blank=True)
    registered_at = models.DateTimeField(
        'Время регистрации',
        default=timezone.now,
        blank=True,
        db_index=True
    )
    called_at = models.DateTimeField(
        'Время звонка',
        null=True,
        blank=True,
        db_index=True
    )
    delivered_at = models.DateTimeField(
        'Время доставки',
        null=True,
        blank=True,
        db_index=True
    )
    pay_method = models.CharField(
        'Способ оплаты',
        max_length=50,
        choices=PAYMENT_CHOICES,
        default='Выяснить',
        db_index=True
    )
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='Заказы',
        related_name='orders',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    objects = OrderQueryset.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.address}'


class OrderItems(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='заказ',
        related_name='order_items',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='товар',
        related_name='order_items',
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(
        'количество',
        validators=[MinValueValidator(1)],
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'

    def __str__(self):
        return f'{self.product.name}, {self.order.firstname}'
