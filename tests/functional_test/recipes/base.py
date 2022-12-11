
from time import sleep

# from django.test import LiveServerTestCase  #SEM O CSS
from django.contrib.staticfiles.testing import \
    StaticLiveServerTestCase  # COM O CSS

from recipes.tests.test_recipe_base import RecipeMixing
from utils.browser import make_chrome_browser as cbrowser


class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixing):
    def setUp(self) -> None:
        self.browser = cbrowser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        sleep(seconds)
