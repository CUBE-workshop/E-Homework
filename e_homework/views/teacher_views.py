from django.shortcuts import render


def teacher(request):
    return render(request, "teacher/teacher.html")
