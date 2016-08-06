from django.core.exceptions import ObjectDoesNotExist
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
    return render(request, "teacher/vote-detail.html", {"vote": Vote.objects.get(id=vote_id)})


def delete_vote(request):
    map(lambda vote_id: Vote.objects.get(id=vote_id[19:-1]).delete(), request.POST['to-delete'].split(','))
    return JsonResponse({})


def do_create_new_vote(request):
    the_vote = Vote.objects.create(name=request.POST['name'], raised_by=Teacher.objects.get(user=request.user),
                                   start_date=request.POST['start-date'], end_date=request.POST['end-date'],
                                   save_name='save-name' in request.POST)
    map(lambda class_id: the_vote.class_invited.add(Class.objects.get(id=class_id)), request.POST['class-choosed'])
    return redirect('/teacher/list')


def modify_vote(request, vote_id):
    the_vote = Vote.objects.get(id=vote_id)
    the_vote.start_date = request.POST['start-date']
    the_vote.end_date = request.POST['end-date']
    the_vote.save()
    return redirect('/teacher/list')


def vote_student_info(request, vote_id):
    student_id = request.POST['student_id']
    ajax_id = request.POST['ajax_id']
    if not Vote.objects.get(id=vote_id).save_name:
        return JsonResponse(
            {'voted': VotePiece.objects.filter(belong_to_vote_id=vote_id, voted_by_id=student_id).exists(),
             'ajax_id': ajax_id})
    else:
        try:
            the_vote = VotePiece.objects.get(belong_to_vote_id=vote_id, voted_by_id=student_id)
            return JsonResponse({'voted': True,
                                 'voted_questions': map(lambda question: question.number,
                                                        the_vote.voted_questions.all()),
                                 'ajax_id': ajax_id})
        except ObjectDoesNotExist:
            return JsonResponse({'voted': False, 'ajax_id': ajax_id})
