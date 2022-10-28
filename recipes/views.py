from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'recipes/home.html', context={'name': 'Lucas'})


def contato(reuqest):
    return HttpResponse('Contato')


def sobre(request):
    a = 2
    a = a + 2
    return HttpResponse(f'sobre + {a}')
