# from django.http import Http404

from os import environ

from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.views.generic import DetailView, ListView

from utils.pagination import make_pagination

from .models import Recipe

# Create your views here.
PER_PAGE = int(environ.get("PER_PAGE"))  # type: ignore


class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        qs = qs.select_related('author', 'category')
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, context.get('recipes'), PER_PAGE, 6)
        context.update({
            'recipes': page_obj,
            'pagination_range': pagination_range,
        })
        return context


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

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id'), is_published=True,
        ).order_by('-id')

        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        recipes = context.get('recipes')
        context.update({
            'title': f'{recipes[0].category.name} - Category | ',
        })
        return context


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            ),
            is_published=True
        ).order_by('-id')

        if not qs:
            raise Http404()

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        context.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'addtional_url_query': f'&q={search_term}',
        })
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = context.get('recipe')
        context.update({
            'recipe': recipe,
            'title': recipe.title,
            'is_detail_page': True,
        })
        return context


class RecipeDetailViewApi(RecipeDetailView):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = recipe_dict['cover'].url
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        return JsonResponse(
            recipe_dict,
            safe=False
        )
