from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from .mutiprocessing_map import map


def number_to_chinese(number):
    """
    将数字转换为中文字符串
    """
    assert 0 < number < 100
    ret = ''
    number_to_chinese_map = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}
    if 10 <= number <= 20:
        ret += '十'
    elif number > 20:
        ret += number_to_chinese_map[number // 10] + '十'
    if number % 10 != 0:
        ret += number_to_chinese_map[number % 10]
    return ret


class School(models.Model):
    """
    保存学校的类型和对应的用户
    """
    SCHOOL_TYPE_CHOICES = (
        ('小', '小学'),
        ('初', '初中'),
        ('高', '高中')
    )
    type = models.CharField(max_length=8, choices=SCHOOL_TYPE_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Class(models.Model):
    """
    保存某个班级是几年级、几班、属于哪个学校
    """
    grade_number = models.PositiveSmallIntegerField()
    class_number = models.PositiveIntegerField()
    school_belong_to = models.ForeignKey(School)

    def str_without_school_name(self):
        """
        :return: 不包含学校名称的班级名称，eg.高一(2)班
        """
        if self.grade_number == 0:
            assert self.school_belong_to.type == '初'
            return '预初' + '(' + str(self.class_number) + ')班'
        return self.school_belong_to.type + number_to_chinese(
            self.grade_number) + '(' + str(self.class_number) + ')班'

    def __str__(self):
        return str(self.school_belong_to) + ' ' + self.str_without_school_name()


class Teacher(models.Model):
    """
    保存教师的身份信息
    """
    school_belong_to = models.ForeignKey(School)
    classes_teaching = models.ManyToManyField(Class)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        permissions = (("teachers_permission", "teachers_permission"),)


class Student(models.Model):
    """
    保存学生的身份信息
    """
    user = models.OneToOneField(User)
    class_belong_to = models.ForeignKey(Class)

    def __str__(self):
        return self.user.username

    @property
    def fullname(self):
        return self.user.first_name + self.user.last_name

    class Meta:
        permissions = (("students_permission", "students_permission"),)
        ordering = ['-class_belong_to']


class Vote(models.Model):
    """
    保存某次问卷的信息
    """
    name = models.CharField(max_length=100)
    raised_by = models.ForeignKey(Teacher)
    class_invited = models.ManyToManyField(Class)
    start_date = models.DateField()
    end_date = models.DateField()
    save_name = models.BooleanField()

    def __str__(self):
        return self.name

    @property
    def is_out_of_date(self):
        """
        :return: 此Vote是否已经过期
        """
        return now().date() > self.end_time

    def is_student_voted(self, student):
        """
        :param student: 要检验的学生对象
        :return: 这个student是已经投票
        """
        return self.votepiece_set.filter(voted_by=student).exists()

    def invited_students(self):
        """
        :return: 被邀请的学生列表
        """
        return sum(map(lambda the_class: list(the_class.student_set.all()),
                       self.class_invited.all()), [])

    def voted_students(self):
        """
        :return: 已经投票的学生列表
        """
        return sum(map(lambda vote_piece: [vote_piece.voted_by],
                       VotePiece.objects.filter(belong_to_vote=self)), [])

    def voted_student_count(self):
        """
        :return: 已投票的学生数量
        """
        return self.votepiece_set.all().count()

    def invited_student_count(self):
        """
        :return: 被邀请的学生数量
        """
        return sum(map(lambda class_: class_.student_set.count(), self.class_invited.all()))


class Question(models.Model):
    """
    保存一个问题的信息
    """
    number = models.SmallIntegerField()
    belong_to_vote = models.ForeignKey(Vote)

    def __str__(self):
        return str(self.belong_to_vote) + ' ' + str(self.number) + '.'

    def voted_student_count(self):
        return self.votepiece_set.all().count()


class VotePiece(models.Model):
    """
    保存一次Vote的信息
    """
    voted_by = models.ForeignKey(Student)
    voted_questions = models.ManyToManyField(Question)
    belong_to_vote = models.ForeignKey(Vote)

    def __str__(self):
        return str(self.voted_by) + ' 对 ' + str(self.belong_to_vote) + ' 的问题'
