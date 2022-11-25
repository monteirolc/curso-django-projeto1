# from unittest import skip

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCateoryViewsTest(RecipeTestBase):
    # TESTES PARA CATEGORY

    def test_recipe_category_views_functions_is_correct(self):

        view = resolve(reverse('recipes:category', args=(1,)))
        self.assertIs(view.func, views.category)

    def test_recipe_category_views_returns_status_code_404_if_no_recipes(self):
        responses = self.client.get(reverse('recipes:category', args=(1000,)))
        self.assertEqual(responses.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        my_title = 'This is my title category'
        self.make_recipe(title=my_title)
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn(my_title, content)
