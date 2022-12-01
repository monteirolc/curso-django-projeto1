# from django.http import Http404

from os import environ

from django.contrib import messages  # noqa ; type: ignore
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.pagination import make_pagination

from .models import Recipe

# Create your views here.
PER_PAGE = int(environ.get("PER_PAGE"))  # type: ignore


def home(request):
    recipes = Recipe.objects.filter(is_published=True,).order_by('-id')
    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGE, 6)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id, is_published=True,).order_by('-id')
    )
    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGE, 6)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{recipes[0].category.name} - Category | '
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'title': recipe.title,
        'is_detail_page': True,
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
    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGE, 6)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'pagination_range': pagination_range,
        'recipes': page_obj,
        'addtional_url_query': f'&q={search_term}',
    })
