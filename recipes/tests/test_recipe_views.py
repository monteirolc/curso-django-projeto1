
from django.urls import resolve, reverse

from recipes import views
from recipes.models import Recipe

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def tearDown(self) -> None:
        return super().tearDown()
    # TESTES PARA HOME

    def test_recipe_home_views_functions_is_correct(self):
        self.make_recipe()
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_views_returns_status_code_200(self):
        self.make_recipe()
        responses = self.client.get(reverse('recipes:home'))
        self.assertEqual(responses.status_code, 200)

    def test_recipe_home_views_loads_correct_template(self):
        self.make_recipe()
        responses = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(responses, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        self.make_recipe()
        Recipe.objects.get(pk=1).delete()
        responses = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes here!',
            responses.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe(preparation_time=10)
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        # self.assertEqual(author.username, 'UserName')
        # self.assertEqual(category.name, 'oneName')
        # self.assertEqual(recipe.title, 'Title of my recipe')
        self.assertIn('Title of my recipe', content)
        self.AssertIn('10 Minuros', content)
        self.assertEqual(len(response_context_recipes), 1)

    # TESTES PARA CATEGORY

    def test_recipe_category_views_functions_is_correct(self):
        self.make_recipe()
        view = resolve(reverse('recipes:category', args=(1,)))
        self.assertIs(view.func, views.category)

    def test_recipe_category_views_returns_status_code_404_if_no_recipes(self):
        responses = self.client.get(reverse('recipes:category', args=(1000,)))
        self.assertEqual(responses.status_code, 404)

    # def test_recipe_category_views_loads_correct_template(self):
    #     responses = self.client.get(reverse('recipes:category', args=(1,)))
    #     self.assertTemplateUsed(responses, 'recipes/pages/category.html')

    # def test_recipe_category_template_shows_no_recipes_found_if_no_recipes(self): # noqa: E501
    #     responses = self.client.get(reverse('recipes:category', args=(1,)))
    #     self.assertIn(
    #         'No recipes here!',
    #         responses.content.decode('utf-8')
    #     )

    # TESTES PARA RECIPE(DETAIL)
    def test_recipe_detail_views_functions_is_correct(self):
        self.make_recipe()
        view = resolve(reverse('recipes:recipe', args=(1,)))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_views_returns_status_code_404_if_no_recipes(self):
        responses = self.client.get(reverse('recipes:recipe', args=(1000,)))
        self.assertEqual(responses.status_code, 404)
