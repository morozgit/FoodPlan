from django.contrib import admin

from .models import Bot_user, Dish, Category, Ingridient, ReceptItem


@admin.register(Bot_user)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'tig_id',
        'subscription_date',
        )
    list_filter = ('subscription_date',)





@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        )
    list_filter = ('name',)


@admin.register(Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'allergen'
        )
    list_filter = ('name', 'allergen')


class ReceptItemInline(admin.TabularInline):
    model = ReceptItem


class DishAdmin (admin.ModelAdmin):
    inlines = [ ReceptItemInline ]
    class Meta:
        model = Dish


admin.site.register(Dish, DishAdmin)







