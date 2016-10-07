from re import compile

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect

from ..models import *
from ..mutiprocessing_map import map


@login_required
@permission_required('e_homework.teachers_permission')
def teacher(request):
    return render(request, "teacher/teacher.html")


@login_required
@permission_required('e_homework.teachers_permission')
def new_vote(request):
    return render(request, "teacher/new-vote.html",
                  {"classes": Teacher.objects.get(user=request.user).classes_teaching.all()})


@login_required
@permission_required('e_homework.teachers_permission')
def vote_list(request):
    return render(request, "teacher/list.html", {"votes": Vote.objects.filter(raised_by__user=request.user)})


@login_required
@permission_required('e_homework.teachers_permission')
def vote_info(request, vote_id):
    the_vote = Vote.objects.get(id=vote_id)
    if the_vote.raised_by != Teacher.objects.get(user=request.user):
        return redirect('/teacher/list/')
    voted_question_count = map(lambda question: question.voted_student_count(),
                               the_vote.question_set.order_by("number"))
    questions_vote_much = sorted(
        filter(lambda question: question.voted_student_count() != 0, the_vote.question_set.order_by("number")),
        key=lambda question: question.voted_student_count(), reverse=True)[:6]
    return render(request, "teacher/vote-detail.html", {"vote": the_vote,
                                                        "questions": list(range(1, the_vote.question_set.count() + 1)),
                                                        "count": voted_question_count,
                                                        "questions_vote_much": questions_vote_much})


@login_required
@permission_required('e_homework.teachers_permission')
def delete_vote(request):
    the_teacher = Teacher.objects.get(user=request.user)
    votes = map(lambda vote_id: Vote.objects.get(id=vote_id[19:-1]), request.POST['to-delete'].split(','))
    map(lambda vote: vote.delete() if vote is not None and vote.raised_by == the_teacher else print('Bad delete'),
        votes)
    return JsonResponse({})


@login_required
@permission_required('e_homework.teachers_permission')
def do_create_new_vote(request):
    the_vote = Vote.objects.create(name=request.POST['name'], raised_by=Teacher.objects.get(user=request.user),
                                   start_date=request.POST['start-date'], end_date=request.POST['end-date'],
                                   save_name='save-name' in request.POST)
    map(lambda class_id: the_vote.class_invited.add(Class.objects.get(id=class_id)), request.POST['class-choosed'])
    map(lambda question_number: Question.objects.create(number=question_number, belong_to_vote=the_vote),
        (number for number in range(1, int(request.POST['question-count']) + 1)))
    return redirect('/teacher/list')


questions_with_tag_re = compile(
    r'<td id="question-(.+?)">(.+?)</td>(.+?)<td>(.+?)</td>')
tags_re = compile(r'<span class="tag">(.+?)</span>')


@login_required
@permission_required('e_homework.teachers_permission')
def modify_vote(request, vote_id):
    the_vote = Vote.objects.get(id=vote_id)
    if the_vote.raised_by != Teacher.objects.get(user=request.user):
        return redirect('/teacher/list/')
    for question in questions_with_tag_re.findall(request.POST['raw-html'].replace('\n', '')):
        question_id = question[0]
        tags = tags_re.findall(question[3])
        the_question = Question.objects.get(id=question_id)
        the_question.tag_set.clear()
        for tag in tags:
            the_tag = Tag.objects.get_or_create(name=tag)[0]
            the_tag.attach_to_questions.add(the_question)
            the_tag.save()
    the_vote.save()
    return redirect('/teacher/list')


@login_required
@permission_required('e_homework.teachers_permission')
def vote_student_info(request, vote_id):
    if Vote.objects.get(id=vote_id).raised_by != Teacher.objects.get(user=request.user):
        return redirect('/teacher/list/')
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
                                                        the_vote.voted_questions.order_by('number')),
                                 'ajax_id': ajax_id})
        except ObjectDoesNotExist:
            return JsonResponse({'voted': False, 'ajax_id': ajax_id})
