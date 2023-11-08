from django.db import models
from django.utils import timezone

from webpage.models import User


class Recipe(models.Model):
    """
    Recipe class model for the Users' recipes.
    """
    # Llave foránea del usuario que escribe la receta
    user: User = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    # Nombre de la receta
    name = models.CharField(max_length=255)
    # Ingredientes
    ingredients = models.TextField()
    # Instrucciones de la preparación
    instructions = models.TextField()
    # Path de la imagen linkeada
    image = models.ImageField(
        upload_to=""
    )
    # Fecha de la publicación
    publish_date = models.DateTimeField(
        default=timezone.localtime,
    )

    def __str__(self):
        return (f"Recipe("
                f"id={self.id}, "
                f"user={self.user.get_username()}, "
                f"name={self.name}"
                f")")


class UserLikesRecipe(models.Model):
    user = models.ForeignKey("webpage.User", on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
