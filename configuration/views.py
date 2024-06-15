import subprocess
from time import sleep
from django.shortcuts import render, redirect
from django.urls import reverse
import os
from django.conf import settings
from configparser import ConfigParser, ParsingError
from django.http import JsonResponse
from django.apps import apps
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from ups.views import page_not_found, unauthorized
from ups.nut2utils import UndefinedError
from .parse import parse_ups, save_ups, parse_upsd, save_upsd, parse_upsmon, save_upsmon


def configure_driver(request, ups):
    if not request.user.is_authenticated:
        return unauthorized(request)

    if request.method == 'POST':
        ups, return_code = save_ups(request.POST, False, ups)
        
        if return_code == 1:
            return redirect(reverse('configuration:configure_driver', kwargs={'ups': ups}))

    ups_info = parse_ups(ups)
    if not ups_info:
        return page_not_found(request)

    context = {'ups_info': ups_info,
               'link_id': 'general',
                'title': ups}

    return render(request, "driver.html", context)

def configure_driver_advanced(request):
    if not request.user.is_authenticated:
        return unauthorized(request)

    if request.method == 'POST':
        return_code = save_ups(request.POST, True)
        
        if return_code == 2:
            return redirect(reverse('configuration:configure_driver_advanced'))

    ups_info = parse_ups(False, True)
    if not ups_info:
        return page_not_found(request)

    context = {'ups_info': ups_info,
               'link_id': 'advanced',
                'title': 'Advanced'}

    return render(request, "driver.html", context)


def configure_upsd(request):
    if not request.user.is_authenticated:
        return unauthorized(request)
    
    if request.method == 'POST':
        return_code = save_upsd(request.POST)
        
        if return_code == 1:
            return redirect(reverse('configuration:configure_upsd'))

    upsd_info = parse_upsd()

    context = {'upsd_info': upsd_info.items(),
               'link_id': 'upsd',
               'title': 'UPSD Config'}

    return render(request, "server.html", context)


def configure_upsmon(request):
    if not request.user.is_authenticated:
        return unauthorized(request)
    
    if request.method == 'POST':
        return_code = save_upsmon(request.POST)
        
        if return_code == 1:
            return redirect(reverse('configuration:configure_upsmon'))

    upsmon_info = parse_upsmon()

    context = {'upsmon_info': upsmon_info.items(),
               'link_id': 'upsmon',
               'title': 'UPSMON Config'}

    return render(request, "monitor.html", context)

