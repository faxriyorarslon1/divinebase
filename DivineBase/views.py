import json

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.authtoken.models import Token

from apps.users.models import User


def configs(request):
    return render(request, 'example.htm')
