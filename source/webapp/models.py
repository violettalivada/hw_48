from django.db import models
from django.core.validators import MinValueValidator


DEFAULT_CATEGORY = 'other'
CATEGORY_CHOICES = (
    (DEFAULT_CATEGORY, 'Разное'),
    ('food', 'Еда'),
    ('tech', 'Бытовая техника'),
    ('tools', 'Инструменты'),
    ('toys', 'Игрушки'),
)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    category = models.CharField(max_length=20, default=DEFAULT_CATEGORY, choices=CATEGORY_CHOICES,
                                verbose_name='Категория')
    amount = models.IntegerField(verbose_name='Остаток', validators=(MinValueValidator(0),))
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2,
                                validators=(MinValueValidator(0),))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Cart(models.Model):
    products = models.ForeignKey('webapp.Product', related_name='cart', on_delete=models.CASCADE)
    qty = models.IntegerField(verbose_name='Количество', validators=(MinValueValidator(0),))

    def __str__(self):
        return f'{self.qty}'

    def get_total(self):
        return self.qty * self.products.price

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Order(models.Model):
    user_name = models.CharField(max_length=100, verbose_name='Имя', null=False, blank=False)
    user_phone = models.CharField(max_length=30, null=False, blank=False, verbose_name='Телефон')
    user_address = models.CharField(max_length=300, null=False, blank=False, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProduct(models.Model):
    product = models.ForeignKey('webapp.Product', related_name='product_orders', on_delete=models.CASCADE,
                                verbose_name='Продукт')
    order = models.ForeignKey('webapp.Order', related_name='order_products', on_delete=models.CASCADE,
                              verbose_name='Заказ')
    qty = models.IntegerField(verbose_name='Количество', validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.order} | {self.product}'
