# from unittest import skip

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    # TESTES PARA HOME
    def test_recipe_home_views_functions_is_correct(self):

        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_views_returns_status_code_200(self):

        responses = self.client.get(reverse('recipes:home'))
        self.assertEqual(responses.status_code, 200)

    def test_recipe_home_views_loads_correct_template(self):

        responses = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(responses, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes here!',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

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

    # TESTES PARA RECIPE(DETAIL)
    def test_recipe_detail_views_functions_is_correct(self):

        view = resolve(reverse('recipes:recipe', args=(1,)))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_views_returns_status_code_404_if_no_recipes(self):
        responses = self.client.get(reverse('recipes:recipe', args=(1000,)))
        self.assertEqual(responses.status_code, 404)

    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
