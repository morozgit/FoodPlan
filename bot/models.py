from django.db import models
from django.contrib.auth.models import User


class UnitOfMeasurement(models.TextChoices):
    GRAM = 'грамм'
    PIECE = 'штука'


class Users(models.Model):
    name = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='users',
                             on_delete=models.CASCADE)
    tig_id = models.CharField(verbose_name='Телеграмм ID', max_length=200) # TODO
    subscription = models.BooleanField(verbose_name='Подписка', default=False)
    subscription_date = models.DateField(verbose_name='Дата подписки',
                                         auto_now=True,
                                         blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(verbose_name='Категории', max_length=200)
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(verbose_name='Блюдо', max_length=200)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='images/', 
                              verbose_name='Изображение')
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 related_name='dishes',
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name


class Favorites(models.Model):
    user_id = models.ForeignKey(Users, verbose_name='Пользователь',
                                related_name='favorites',
                                on_delete=models.CASCADE,)
    dish_id = models.ForeignKey(Dish, verbose_name='Блюдо',
                                related_name='favorites',
                                on_delete=models.CASCADE,)
    
    class Meta:
        verbose_name = 'Избранное'

    def __str__(self):
        return f'{self.user_id}, {self.dish_id}'


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Ингридиент', max_length=200)
    count = models.IntegerField(verbose_name='ID', db_index=True)
    image = models.ImageField(upload_to='images/', 
                              verbose_name='Изображение')
    allergen = models.BooleanField(verbose_name='Аллерген', default=False)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    dish_id = models.ForeignKey(Dish, verbose_name='ID Блюда',
                                related_name='recipes',
                                on_delete=models.CASCADE,)
    ingredient_id = models.ManyToManyField(Ingredient, verbose_name='Категории',
                                           related_name='recipes')
    col_ingredient = models.FloatField(verbose_name='Количество')
    unit = models.CharField(
        max_length=10,
        choices=UnitOfMeasurement.choices,
        default=UnitOfMeasurement.GRAM
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.dish_id.name


class Pay(models.Model):
    user_id = models.ForeignKey(Users, verbose_name='Пользователь',
                                related_name='pays',
                                on_delete=models.CASCADE,)
    sum = models.FloatField(verbose_name='Сумма')
    date_time = models.DateTimeField(verbose_name='Дата и время оплаты',
                                     auto_now_add=True)
    
    class Meta:
        verbose_name = 'Оплата'

    def __str__(self):
        return f'{self.user_id}, {self.sum}, {self.date_time}'
