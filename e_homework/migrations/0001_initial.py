# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 23:53
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_number', models.PositiveSmallIntegerField()),
                ('class_number', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('', '小学'), ('初', '初中'), ('高', '高中')], max_length=8)),
                (
                'user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_belong_to',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_homework.Class')),
                (
                'user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('students_permission', 'students_permission'),),
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes_teaching', models.ManyToManyField(to='e_homework.Class')),
                ('school_belong_to',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_homework.School')),
                (
                'user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('teachers_permission', 'teachers_permission'),),
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_time', models.DateField()),
                ('end_time', models.DateField()),
                ('save_name', models.BooleanField()),
                ('raised_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_homework.Teacher')),
                ('students_invited', models.ManyToManyField(to='e_homework.Student')),
            ],
        ),
        migrations.CreateModel(
            name='VotePiece',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                'belong_to_vote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_homework.Vote')),
                ('voted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_homework.Student')),
                ('voted_questions', models.ManyToManyField(to='e_homework.Question')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='belong_to_vote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_homework.Vote'),
        ),
        migrations.AddField(
            model_name='class',
            name='school_belong_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_homework.School'),
        ),
    ]
