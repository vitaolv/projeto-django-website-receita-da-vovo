import os

from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView

from recipes.models import Recipe
from tag.models import Tag
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 8))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            is_published=True,
        )

        query_set = query_set.select_related(
            'author', 'category', 'author__profile')
        query_set = query_set.prefetch_related('tags')

        return query_set

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            context_data.get('recipes'),
            PER_PAGE,
        )

        html_language = translation.get_language()

        context_data.update(
            {
                'recipes': page_obj,
                'pagination_range': pagination_range,
                'html_language': html_language,
            }
        )
        return context_data


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()

        return JsonResponse(
            list(recipes_list),
            safe=False
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        category_translation = _('Category')

        context_data.update(
            {
                'title': f'{context_data.get("recipes")[0].category.name} - '
                f'{category_translation} | '
            }
        )
        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            category__id=self.kwargs.get('category_id'),
        )

        if not queryset:
            raise Http404()

        return queryset


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            Q(
                Q(title__icontains=search_term) | Q(
                    description__icontains=search_term)
            )
        )

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        context.update({
            'page_title': f'Pesquisa por "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })
        return context


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'is_detali_page': True,
        })
        return context


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri(
            ) + recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            tags__slug=self.kwargs.get('slug', ''),
        )
        return query_set

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')
        ).first()

        if not page_title:
            page_title = 'Sinto muito! N??o h?? receita encontrada.'

        page_title = f'{page_title} - Tag |'
        context.update({
            'page_title': page_title,
        })
        return context


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id,
                               is_published=True,
                               )

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detali_page': True,
    })


def about(request):
    return render(request, 'recipes/pages/about.html')
