from django.contrib import admin

import recipes.models


@admin.register(recipes.models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")


@admin.register(recipes.models.UserLikesRecipe)
class UserLikesRecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recipe")
