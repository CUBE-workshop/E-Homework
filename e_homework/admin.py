from django.contrib import admin

from .models import *

admin.site.register(School)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Vote)
admin.site.register(Question)
admin.site.register(VotePiece)

# Register your models here.
