from time import sleep

# from django.test import LiveServerTestCase  #SEM O CSS
from django.contrib.staticfiles.testing import \
    StaticLiveServerTestCase  # COM O CSS

from utils.browser import make_chrome_browser as cbrowser


class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = cbrowser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        sleep(seconds)
