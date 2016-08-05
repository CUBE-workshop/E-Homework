from django.http import JsonResponse
from django.shortcuts import render, redirect

from ..models import *
from ..mutiprocessing_map import map


def teacher(request):
    return render(request, "teacher/teacher.html")


def new_vote(request):
    return render(request, "teacher/new-vote.html",
                  {"classes": Teacher.objects.get(user=request.user).classes_teaching.all()})


def vote_list(request):
    return render(request, "teacher/list.html", {"votes": Vote.objects.filter(raised_by__user=request.user)})


def vote_info(request, vote_id):
    print(request, vote_id)


def delete_vote(request):
    map(lambda vote_id: Vote.objects.get(id=vote_id[6:]).delete(), request.POST['to-delete'].split(','))
    return JsonResponse({})


def do_create_new_vote(request):
    the_vote = Vote.objects.create(name=request.POST['name'], raised_by=Teacher.objects.get(user=request.user),
                                   start_date=request.POST['start-date'], end_date=request.POST['end-date'],
                                   save_name='save-name' in request.POST)
    map(lambda class_id: the_vote.class_invited.add(Class.objects.get(id=class_id)), request.POST['class-choosed'])
    return redirect('/teacher/list')
