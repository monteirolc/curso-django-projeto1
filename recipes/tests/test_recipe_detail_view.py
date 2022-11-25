# from unittest import skip

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewsTest(RecipeTestBase):
    # TESTES PARA RECIPE(DETAIL)
    def test_recipe_detail_views_functions_is_correct(self):

        view = resolve(reverse('recipes:recipe', args=(1,)))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_views_returns_status_code_404_if_no_recipes(self):
        responses = self.client.get(reverse('recipes:recipe', args=(1000,)))
        self.assertEqual(responses.status_code, 404)
