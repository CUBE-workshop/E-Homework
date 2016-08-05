from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password as try_validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from e_homework.models import *


def get_school_list(_):
    school_list = list(map(lambda school: {'id': school.id, 'name': school.user.username}, School.objects.all()))
    return JsonResponse({'school_list': school_list})


def get_class_list(request):
    class_list = list(map(lambda class_: {'id': class_.id, 'name': class_.str_without_school_name()},
                          School.objects.get(id=request.POST['school-id']).class_set.all()))
    return JsonResponse({'class_list': class_list})


def validate_username(request):
    the_username = request.POST['username']
    return JsonResponse(
        {'is_valid': not User.objects.filter(username=the_username).exists(), 'ajax_id': request.POST['ajax_id']})


def validate_password(request):
    try:
        try_validate_password(request.POST['password'])
    except (ValidationError, ValueError, MultiValueDictKeyError):
        return JsonResponse({'is_valid': False, 'ajax_id': request.POST['ajax_id']})
    return JsonResponse({'is_valid': True, 'ajax_id': request.POST['ajax_id']})


def validate_user(request):
    return JsonResponse({'is_valid': User.objects.filter(username=request.POST['username']).exists(),
                         'ajax_id': request.POST['ajax_id']})


def validate_password_for_user(request):
    username = request.POST['username']
    password = request.POST['password']
    return JsonResponse(
        {'is_valid': not (authenticate(username=username, password=password) is None),
         'ajax_id': request.POST['ajax_id']})


def sign_in(request):
    return render(request, "sign-in.html")


def sign_up(request):
    return render(request, "sign-up.html")


def do_sign_up(request):
    username = request.POST['username']
    password = make_password(request.POST['password'])
    if request.POST['user-type'] == 'school':
        School.objects.create(type=request.POST['school-type'],
                              user=User.objects.create(username=username, password=password))
    elif request.POST['user-type'] == 'teacher':
        the_teacher = Teacher.objects.create(school_belong_to=School.objects.get(id=request.POST['school-in']),
                                             user=User.objects.create(username=username, password=password,
                                                                      first_name=request.POST['first-name'],
                                                                      last_name=request.POST['last-name']))
        teachers_user_group, _ = Group.objects.get_or_create(name='teachers_user_group')
        teachers_user_group.permissions.add(Permission.objects.get(name='teachers_permission'))
        the_teacher.user.groups.add(teachers_user_group)
    else:
        the_student = Student.objects.create(class_belong_to=Class.objects.get(id=request.POST['class-in']),
                                             user=User.objects.create(username=username, password=password,
                                                                      first_name=request.POST['first-name'],
                                                                      last_name=request.POST['last-name']))
        students_user_group, _ = Group.objects.get_or_create(name='students_user_group')
        students_user_group.permissions.add(Permission.objects.get(name='students_permission'))
        the_student.user.groups.add(students_user_group)

    return redirect('/sign-in/')


def do_sign_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        if Teacher.objects.filter(user=user).exists():
            return redirect('/teacher/')
        elif Student.objects.filter(user=user).exists():
            return redirect('/student/')
    else:
        return HttpResponseForbidden


def do_logout(request):
    logout(request)
    return redirect('/sign-in/')
