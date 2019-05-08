# -*- coding:utf-8
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404

# Create your views here.
from plate.models import Plate
from toolbar.models import Toolbar


def index(request):
    plate = Plate.objects.filter(status__gt=0).all()
    first = None
    if plate:
        first = plate[0].id
    return render(request, 'toolkit/index.html', {'plate': plate, 'first': first})


def list(request, sid):
    plate = get_object_or_404(Plate, pk=sid)
    return render(request, 'toolkit/list.html', {'plate': plate})
