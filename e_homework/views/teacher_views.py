from django.http import JsonResponse
from django.shortcuts import render

from ..models import *


def teacher(request):
    return render(request, "teacher/teacher.html")


def vote_list(request):
    return render(request, "teacher/list.html", {"votes": Vote.objects.filter(raised_by__user=request.user)})


def vote_info(request, vote_id):
    print(request, vote_id)


def delete_vote(request):
    map(lambda vote_id: Vote.objects.get(id=vote_id[6:]).delete(), request.POST['to-delete'].split(','))
    return JsonResponse({})
