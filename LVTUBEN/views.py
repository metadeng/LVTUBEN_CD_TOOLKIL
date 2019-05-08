# coding:utf-8
from django.shortcuts import render_to_response


def page_not_found(request, exception):
    model = str(request.path).split('/')[2]
    return render_to_response(request, '404.html', {'model': model, 'exception': exception})
