from django.shortcuts import render

from ..models import *


def teacher(request):
    return render(request, "teacher/teacher.html")


def vote_list(request):
    return render(request, "teacher/list.html", {"votes": Vote.objects.filter(raised_by__user=request.user)})


def vote_info(request, vote_id):
    print(request, vote_id)
