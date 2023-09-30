from django.contrib import admin

from .models import Users, Dish, Category, Favorites, Ingredient, Recipe, Pay


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'tig_id',
        'subscription_date',
        )
    list_filter = ('subscription_date',)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'category_id',
        )
    list_filter = ('category_id',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        )


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'dish_id',
        )
    list_filter = (
        'user_id', 
        'dish_id'
        )

    raw_id_fields = (
        'user_id',
        'dish_id'
        )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'count',
        'allergen'
        )
    list_filter = (
        'allergen', 
        )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'dish_id',
        'col_ingredient',
        'unit'
        )
    list_filter = (
        'dish_id', 
        'ingredient_id',
        )
    raw_id_fields = (
        'dish_id', 
        'ingredient_id',
        )


@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'sum',
        'date_time',
        )
    list_filter = (
        'user_id', 
        'date_time',
        )
    raw_id_fields = (
        'user_id', 
        )
