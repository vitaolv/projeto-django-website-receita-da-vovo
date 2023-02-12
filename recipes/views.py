import os

from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import ListView

from recipes.models import Recipe
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
        return query_set

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            context_data.get('recipes'),
            PER_PAGE,
        )
        context_data.update({
            'recipes': page_obj,
            'pagination_range': pagination_range,
        })
        return context_data


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id,
                               is_published=True,
                               )

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detali_page': True,
    })


def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True,
    ).order_by('-id')
    )

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - Category | '
    })


def search(request):

    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(
        request,
        'recipes/pages/search.html',
        {'page_title': f'Pesquisa por "{search_term}"',
         'search_term': search_term,
         'recipes': page_obj,
         'pagination_range': pagination_range,
         'additional_url_query': f'&q={search_term}',
         }
    )


def about(request):
    return render(request, 'recipes/pages/about.html')
