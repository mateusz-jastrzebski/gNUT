from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from django.apps import apps
from .nut2utils import UndefinedError


def home(request):
    app_config = apps.get_app_config('ups')
    ups_list = app_config.ups_list

    context = {'ups_list': ups_list,
               'link_id': 'general',
               'title': "UPS List"}
    if request.user.is_authenticated:
        base_template_name = 'base_admin.html'
    else:
        base_template_name = 'base.html'
    context['base_template_name'] = base_template_name
    return render(request, 'home.html', context)


def ups_view(request, ups):
    app_config = apps.get_app_config('ups')
    try:
        ups_vars = app_config.webnut.get_ups_vars(ups)
    except UndefinedError:
        return page_not_found(request)

    context = {'ups_vars': ups_vars[0],
               'ups_status': ups_vars[1],
               'ups_batt': ups_vars[0]['battery.charge'][0],
               'link_id': 'general',
               'title': ups}
    if request.user.is_authenticated:
        base_template_name = 'base_admin.html'
    else:
        base_template_name = 'base.html'
    context['base_template_name'] = base_template_name
    return render(request, 'ups_view.html', context)


def get_ups_list(request):
    app_config = apps.get_app_config('ups')
    ups_list = app_config.ups_list

    return JsonResponse({'ups_list': ups_list})


def page_not_found(request):
    return render(request, '404.html', status=404)


def unauthorized(request):
    return render(request, '401.html', status=401)
