from django.urls import path

from . import views

urlpatterns = [
    path('', views.RecetasView.as_view(), name="recipes"),
    path('created-recipes/', views.RecetasCreadasView.as_view(), name="created-recipes"),
    path('saved-recipes/', views.RecetasGuardadasView.as_view(), name="saved-recipes"),
    path('<int:recipe_id>/', views.LecturaRecetaView.as_view(), name="recipe"),
    path('new/', views.NewRecipeView.as_view(), name="new-recipe"),
    path('edit/<int:recipe_id>/', views.EditRecipeView.as_view(), name="edit-recipe"),
    path('search', views.SearchRecipesView.as_view(), name="search-result"),
]
