from django.contrib import admin

from .models import Category, Recipe


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)  # Deste jeito
class RecipeAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)   # Ou desse jeito
