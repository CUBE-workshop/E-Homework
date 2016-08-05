from django.test import TestCase

from e_homework.views.auth_views import *


class FakeRequest:
    pass


class GetClassListTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='A', password='')
        self.school1 = School.objects.create(type='高', user=self.user1)
        self.user2 = User.objects.create(username='B', password='')
        self.school2 = School.objects.create(type='初', user=self.user2)
        self.class1 = Class.objects.create(grade_number=1, class_number=1, school_belong_to=self.school1)
        self.class2 = Class.objects.create(grade_number=1, class_number=2, school_belong_to=self.school1)
        self.class3 = Class.objects.create(grade_number=1, class_number=3, school_belong_to=self.school2)

    def test_get(self):
        fake_request = FakeRequest()
        setattr(fake_request, 'POST', {'school-id': self.school1.id})
        response = get_class_list(fake_request)
        self.assertEqual(response.content, JsonResponse(
            {"class_list": [
                {'id': self.class1.id, 'name': self.class1.str_without_school_name()},
                {'id': self.class2.id, 'name': self.class2.str_without_school_name()}
            ]}).content)
