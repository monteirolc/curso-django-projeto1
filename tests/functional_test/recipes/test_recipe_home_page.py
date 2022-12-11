from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctinalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_messages(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes here!', body.text)

    def test_recipe_search_home_can_find_a_recipe(self):
        recipes = self.make_recipe_in_batch(qtd=20)
        self.browser.get(self.live_server_url)
        search = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Search for a recipe"]'
        )
        search.click()
        search.send_keys(recipes[0].title)
        search.send_keys(Keys.ENTER)
        self.assertIn(recipes[0].title, self.browser.find_element(
            By.CLASS_NAME, 'main-content-list').text)

    @patch('recipes.views.PER_PAGE', new=4)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch(20)
        self.browser.get(self.live_server_url)
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            4

        )
