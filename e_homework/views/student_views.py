from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect

from ..models import *


@login_required
@permission_required('e_homework.students_permission')
def student(request):
    the_student = Student.objects.get(user=request.user)
    votes_invite_the_student = Vote.objects.filter(class_invited=the_student.class_belong_to)
    votes_voted_by_the_student = VotePiece.objects.filter(voted_by=the_student)
    return render(request, "student/student.html", {
        'unvote_count': votes_invite_the_student.count() - votes_voted_by_the_student.count(),
        'votes': votes_invite_the_student,
        'student': the_student
    })


@login_required
@permission_required('e_homework.students_permission')
def vote(request, vote_id):
    the_student = Student.objects.get(user=request.user)
    the_vote = Vote.objects.get(id=vote_id)
    if the_student not in the_vote.invited_students():
        return redirect('/student/')
    votes_invite_the_student = Vote.objects.filter(class_invited=the_student.class_belong_to)
    return render(request, "student/vote.html", {
        'vote': the_vote,
        'unvote_count': votes_invite_the_student.count() - VotePiece.objects.filter(
            voted_by=the_student).count(),
        'votes': votes_invite_the_student,
        'student': the_student
    })


@login_required
@permission_required('e_homework.students_permission')
def do_vote(request, vote_id):
    the_student = Student.objects.get(user=request.user)
    the_vote = Vote.objects.get(id=vote_id)
    if the_student not in the_vote.invited_students():
        return redirect('/student/')
    the_vote_piece = VotePiece.objects.get_or_create(voted_by=Student.objects.get(user=request.user),
                                                     belong_to_vote=Vote.objects.get(id=vote_id))[0]
    the_vote_piece.voted_questions.clear()
    for question_id in filter(lambda post_item: post_item != 'csrfmiddlewaretoken', request.POST):
        the_vote_piece.voted_questions.add(Question.objects.get(id=question_id))
    return redirect('/student/')
