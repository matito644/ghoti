from django import forms

from recipes import models


class NewRecipeForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = ["name", "image", "ingredients", "instructions"]

    def __init__(self, *args, **kwargs):
        super(NewRecipeForm, self).__init__(*args, **kwargs)
        self.fields["image"].required = False
