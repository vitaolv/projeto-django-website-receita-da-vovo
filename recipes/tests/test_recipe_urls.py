from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_home_url_is_correct(self):
        home_url = reverse('recipes:home')
        self.assertEqual(home_url, '/')

    def test_recipe_home_url_is_correct(self):
        recipe_home_url = reverse(
            'recipes:category', kwargs={'category_id': 1})
        self.assertEqual(recipe_home_url, '/recipes/category/1/')

    def test_recipe_detali_url_is_correct(self):
        recipe_detali_url = reverse(
            'recipes:recipe', kwargs={'id': 1})
        self.assertEqual(recipe_detali_url, '/recipes/1/')

    def test_recipe_search_url_is_correct(self):
        recipe_search_url = reverse('recipes:search')
        self.assertEqual(recipe_search_url, '/recipes/search/')
