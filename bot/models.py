from django.db import models
from django.contrib.auth.models import User


class UnitOfMeasurement(models.TextChoices):
    GRAM = "грамм"
    PIECE = "штука"
    KG = "Киллограмм"
    

class Category(models.Model):
    name = models.CharField(verbose_name="Категории", max_length=200)
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Ingridient(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    allergen = models.BooleanField(verbose_name="Аллерген", default=False)
    price = models.FloatField(verbose_name="Цена")

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return self.name


class Dish(models.Model):

    name = models.CharField(verbose_name="Блюдо", max_length=200)
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to="images/", verbose_name="Изображение", blank=True, null=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        related_name="dishes",
        on_delete=models.CASCADE,
    )
    ingridients = models.ManyToManyField(
       Ingridient, related_name='Dishes', blank=True, through="ReceptItem"
    )

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    def __str__(self):
        return self.name


class ReceptItem(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingridient = models.ForeignKey(Ingridient, verbose_name="Ингридиент",  on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Количество")
    unit = models.CharField(max_length=255, choices=UnitOfMeasurement.choices, 
                            verbose_name="Единица измерения", 
                            default='PIECE')

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"


class Bot_user(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=200, null=True)
    tig_id = models.CharField(verbose_name="Телеграмм ID", max_length=200)
    subscription_date = models.DateField(
        verbose_name="Дата подписки", auto_now=False, blank=True, null=True
    )
    favorites = models.ManyToManyField(Dish, related_name='DishesLikes')

    class Meta:
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.tig_id} {self.name}"


class Pay(models.Model):
    user = models.ForeignKey(Bot_user, related_name="Users_pays", verbose_name= "Пользователь", on_delete=models.CASCADE)
    pay_date = models.DateTimeField(auto_now=False, verbose_name="Дата оплаты")
    summ = models.FloatField(default=100)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user.name} {self.pay_date}"

