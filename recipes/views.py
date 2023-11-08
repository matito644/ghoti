import abc

import django.views.generic.base
from django import shortcuts
from django.http import HttpResponseRedirect
from django.views import generic

from . import forms
from . import models


class Buscador(django.views.generic.base.View, abc.ABC):
    """
    Abstract class that provides a class the functionality of search a word using the search bar.
    """

    def filter_search(self, view_context, filter_name='recipes'):
        """
        Filter the view_context given the name of the filtered value.

        :param view_context: A dictionary that works as context.
        :param filter_name: A name that works as a key of the view context.
        :return: the view_context filtered.
        """
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            view_context[filter_name] = view_context[filter_name].filter(name__icontains=search_input)
        return view_context


class LecturaRecetaView(generic.TemplateView):
    """
    Recipe Reading View class.

    Handles the view's requests.
    """

    # noinspection PyMethodOverriding
    def get(self, request, recipe_id):
        """
        Manage a get request.

        Returns:
            A rendered view with the recipe template.
        """

        try:
            recipe = models.Recipe.objects.get(id=recipe_id)
        except models.Recipe.DoesNotExist:
            return shortcuts.render(request, "display.html")

        view_context = {
            "recipe": recipe
        }

        if request.user.is_authenticated:
            # noinspection PyUnresolvedReferences
            view_context["is_saved"] = models.UserLikesRecipe.objects.filter(user=request.user, recipe=recipe).exists()

        return shortcuts.render(request, "recipe.html", context=view_context)

    # noinspection PyMethodMayBeStatic
    def post(self, request, recipe_id):
        try:
            recipe = models.Recipe.objects.get(id=recipe_id)
        except models.Recipe.DoesNotExist:
            return shortcuts.render(request, "display.html")

        save = request.POST["saved"] == "true"
        if save:
            # noinspection PyUnresolvedReferences
            like, created = models.UserLikesRecipe.objects.get_or_create(user=request.user, recipe=recipe)
            like.save()
        else:
            # noinspection PyUnresolvedReferences
            like = models.UserLikesRecipe.objects.filter(user=request.user, recipe=recipe)
            if like.exists():
                like.first().delete()

        try:
            recipe = models.Recipe.objects.get(id=recipe_id)
        except models.Recipe.DoesNotExist:
            return shortcuts.render(request, "display.html")

        # noinspection PyUnresolvedReferences
        view_context = {
            "recipe": recipe,
            "is_saved": models.UserLikesRecipe.objects.filter(user=request.user, recipe=recipe).exists()
        }

        return shortcuts.render(request, "recipe.html", context=view_context)


class RecetasView(generic.TemplateView, Buscador):
    """
    Recipes Display View class.

    Handles the view's requests.
    """

    # noinspection PyMethodOverriding
    def get(self, request):
        """
        Manage a get request.

        Returns:
            A rendered view with the recipes display.
        """

        recipes_list = models.Recipe.objects.all()

        view_context = self.filter_search({
            "recipes": recipes_list
        }, filter_name='recipes')

        return shortcuts.render(request, "display.html", context=view_context)


class RecetasCreadasView(generic.TemplateView, Buscador):
    """
    Own recipes Display View class.

    Handles the view's requests.
    """

    # noinspection PyMethodOverriding
    def get(self, request):
        """
        Manage a get request.

        Returns:
            A rendered view with the recipes display.
        """

        recipes_list = models.Recipe.objects.filter(user=request.user)

        view_context = self.filter_search({
            "recipes": recipes_list
        }, filter_name='recipes')

        return shortcuts.render(request, "display.html", context=view_context)


class RecetasGuardadasView(generic.TemplateView, Buscador):
    """
    Saved recipes Display View class.

    Handles the view's requests.
    """

    # noinspection PyMethodOverriding
    def get(self, request):
        """
        Manage a get request.

        Returns:
            A rendered view with the recipes display.
        """

        # noinspection PyUnresolvedReferences
        recipes_list = [x.recipe for x in models.UserLikesRecipe.objects.filter(user=request.user)]

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            recipes_list = [recipe for recipe in recipes_list if search_input.lower() in recipe.name.lower()]

        view_context = {
            "recipes": recipes_list
        }

        return shortcuts.render(request, "display.html", context=view_context)


class NewRecipeView(generic.TemplateView):
    """
    New Recipe View class.

    Handles the view's requests.
    """

    # noinspection PyMethodOverriding
    def get(self, request):
        """
        Manage a get request.

        Returns:
            A rendered view with the new recipe form.
        """

        recipe_form = forms.NewRecipeForm()
        if not request.user.is_authenticated:
            return HttpResponseRedirect(f"/recipes/")

        view_context = {
            "form": recipe_form
        }

        return shortcuts.render(request, "new.html", context=view_context)

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        """
        Manage the form submit.

        Returns:
            A rendered view with the created recipe.
        """

        recipe_data = forms.NewRecipeForm(request.POST, request.FILES)

        if recipe_data.is_valid():
            recipe_data = recipe_data.cleaned_data
            recipe = models.Recipe(
                user=request.user,
                name=recipe_data["name"],
                ingredients=recipe_data["ingredients"],
                instructions=recipe_data["instructions"],
                image=recipe_data["image"]
            )

            recipe.save()

            return HttpResponseRedirect(f"/recipes/{recipe.id}")

        return HttpResponseRedirect("/recipes/new/")


class EditRecipeView(generic.TemplateView):
    """
    Edit Recipe View class.

    Handles the view's requests.
    """

    # noinspection PyMethodOverriding
    def get(self, request, recipe_id):
        """
        Manage a get request.

        Returns:
            A rendered view with the edit recipe form.
        """

        try:
            recipe = models.Recipe.objects.get(id=recipe_id)
        except models.Recipe.DoesNotExist:
            return HttpResponseRedirect(f"/recipes/{recipe_id}")

        if request.user != recipe.user:
            return HttpResponseRedirect(f"/recipes/{recipe_id}")

        recipe_form = forms.NewRecipeForm(instance=recipe)

        view_context = {
            "form": recipe_form,
            "recipe_id": recipe_id,
        }

        return shortcuts.render(request, "edit.html", context=view_context)

    # noinspection PyMethodMayBeStatic
    def post(self, request, recipe_id):
        """
        Manage the form submit.

        Returns:
            A rendered view with the created recipe.
        """

        recipe_data = forms.NewRecipeForm(request.POST, request.FILES)
        recipe = models.Recipe.objects.get(id=recipe_id)
        if recipe_data.is_valid():
            recipe_data = recipe_data.cleaned_data

            recipe.user = request.user
            recipe.name = recipe_data["name"]
            recipe.ingredients = recipe_data["ingredients"]
            recipe.instructions = recipe_data["instructions"]
            if not recipe_data["image"] is None:
                recipe.image = recipe_data["image"]

            recipe.save()

            return HttpResponseRedirect(f"/recipes/{recipe.id}")

        return HttpResponseRedirect(f"/recipes/edit/{recipe.id}")


class SearchRecipesView(generic.ListView):
    model = models.Recipe
    template_name = 'search_results.html'
    ...
