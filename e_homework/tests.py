from django.contrib.auth.models import Permission, Group
from django.test import LiveServerTestCase

from .models import *


class TagInfoTest(LiveServerTestCase):
    def setUp(self):
        self.school = School.objects.create(type='高', user=User.objects.create(username='test_school', password=''))
        self._class = Class.objects.create(grade_number=1, class_number=1, school_belong_to=self.school)
        self.teacher = Teacher.objects.create(school_belong_to=self.school,
                                              user=User.objects.create(username='test_teacher', password=''))
        self.teacher.classes_teaching.add(self._class)
        teachers_user_group, _ = Group.objects.get_or_create(name='teachers_user_group')
        teachers_user_group.permissions.add(Permission.objects.get(name='teachers_permission'))
        self.teacher.user.groups.add(teachers_user_group)
        self.student1 = Student.objects.create(user=User.objects.create(username='test_student1', password=''),
                                               class_belong_to=self._class)
        self.student2 = Student.objects.create(user=User.objects.create(username='test_student2', password=''),
                                               class_belong_to=self._class)
        students_user_group, _ = Group.objects.get_or_create(name='students_user_group')
        students_user_group.permissions.add(Permission.objects.get(name='students_permission'))
        self.student1.user.groups.add(students_user_group)
        self.student2.user.groups.add(students_user_group)
        self.vote = Vote.objects.create(name='test_vote',
                                        raised_by=self.teacher,
                                        start_date=now().date(),
                                        end_date=now().date(),
                                        save_name=True)
        self.vote.class_invited.add(self._class)
        self.questions = [Question.objects.create(number=i, belong_to_vote=self.vote) for i in range(21)]
        self.vote_piece1 = VotePiece.objects.create(voted_by=self.student1, belong_to_vote=self.vote)
        self.vote_piece2 = VotePiece.objects.create(voted_by=self.student2, belong_to_vote=self.vote)
        self.vote_piece1.voted_questions.set(
            [self.questions[0], self.questions[2], self.questions[4], self.questions[6], self.questions[8],
             self.questions[19], self.questions[20]])
        self.vote_piece2.voted_questions.set(
            [self.questions[0], self.questions[1], self.questions[2], self.questions[6], self.questions[8],
             self.questions[19], self.questions[20]])
        self.tags = [Tag.objects.create(name=chr(ord('a') + n)) for n in range(7)]
        self.tags[0].attach_to_questions.add(self.questions[0])
        self.tags[1].attach_to_questions.add(self.questions[2])
        self.tags[2].attach_to_questions.add(self.questions[6])
        self.tags[3].attach_to_questions.add(self.questions[8])
        self.tags[4].attach_to_questions.add(self.questions[19])
        self.tags[5].attach_to_questions.add(self.questions[20])
        self.tags[6].attach_to_questions.add(self.questions[1])


class TeacherTagInfoTest(TagInfoTest):
    def test_tag(self):
        self.assertEqual(self.tags[0].vote_people_count(), 2)
        self.assertEqual(self.tags[1].vote_people_count(), 2)
        self.assertEqual(self.tags[6].vote_people_count(), 1)

    def test_can_get_class_info(self):
        self.client.force_login(User.objects.get(username='test_teacher'))
        response = self.client.get('/teacher/tag-info/')
        self.assertContains(response, '<th>a</th>')
        self.assertContains(response, '<th>b</th>')
        self.assertContains(response, '<th>c</th>')
        self.assertContains(response, '<th>d</th>')
        self.assertContains(response, '<th>e</th>')
        self.assertContains(response, '<th>f</th>')
        self.assertContains(response, '<th>g</th>')
        self.assertContains(response, '高一(1)班')

    def test_can_switch_class(self):
        self.client.force_login(User.objects.get(username='test_teacher'))
        response = self.client.post('/teacher/tag-info/', {'class': self._class.id})
        self.assertIn({'question_count': 2, 'name': 'f'}, response.json()['tags'])
        self.assertIn({'question_count': 2, 'name': 'b'}, response.json()['tags'])
        self.assertIn({'question_count': 1, 'name': 'g'}, response.json()['tags'])


class StudentTagInfoTest(TagInfoTest):
    def test_question_is_voted(self):
        self.assertTrue(self.questions[0].voted_by_student(self.student1))
        self.assertFalse(self.questions[1].voted_by_student(self.student1))

    def test_tag_is_voted(self):
        self.assertTrue(self.tags[0].voted_by_student(self.student1))
        self.assertFalse(self.tags[6].voted_by_student(self.student1))

    def test_can_get_tag_info(self):
        self.client.force_login(User.objects.get(username='test_student1'))
        response = self.client.get('/student/tag-info/')
        self.assertContains(response, '<tr><th>a</th><th>1</th></tr>', html=True)
        self.assertContains(response, '<tr><th>b</th><th>1</th></tr>', html=True)
        self.assertContains(response, '<tr><th>c</th><th>1</th></tr>', html=True)
        self.assertContains(response, '<tr><th>d</th><th>1</th></tr>', html=True)
        self.assertContains(response, '<tr><th>e</th><th>1</th></tr>', html=True)
        self.assertContains(response, '<tr><th>f</th><th>1</th></tr>', html=True)
        self.assertNotContains(response, '<th>g</th>')
