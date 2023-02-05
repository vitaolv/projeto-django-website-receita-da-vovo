from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.sleep()
        self.assertIn('Sinto muito! Não há receita encontrada.', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_cam_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'Qualquer um título'

        recipes[0].title = title_needed
        recipes[0].save()

        self.browser.get(self.live_server_url)

        search_input = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Encontre uma receita aqui..."]')

        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        self.sleep()
        self.assertIn(title_needed,
                      self.browser.find_element(
                          By.CLASS_NAME, 'main-content-list').text,
                      )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        self.browser.get(self.live_server_url)
        self.sleep(5)
        goToPage2 = self.browser.find_element(
            By.XPATH, '//a[@aria-label="Ir para página 2"]')
        self.sleep(5)
        self.browser.execute_script("arguments[0].click();", goToPage2)

        self.sleep(5)
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'receita')), 2)
