from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from time import sleep


class TagInfoTest(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        # 测试教师开始了一个vote
        self.start_a_vote()
        # 测试学生1登录了网站
        self.login('functional_test_student1', 'TDD is good')
        # 测试学生1做了Vote [1, 2, 3, 5, 7, 9, 11, 22]
        self.do_vote([1, 2, 3, 5, 7, 9, 11, 22])
        # 测试学生2登录了网站
        self.login('functional_test_student2', 'TDD is good')
        # 测试学生2做了Vote [1, 2, 3, 5, 4, 9, 22]
        self.do_vote([1, 2, 3, 5, 4, 9, 22])
        # 测试学生3登录了网站
        self.login('functional_test_student3', 'TDD is good')
        # 测试学生3做了Vote [9, 22]
        self.do_vote([9, 22])
        # 测试教师给Vote添加了Tag
        self.add_tags()

    def login(self, username, password):
        self.browser.get('http://localhost:8000/sign-in/')
        sleep(1)
        self.browser.find_element_by_id('username').send_keys(username)
        self.browser.find_element_by_id('password').send_keys(password)
        sleep(3)
        self.browser.find_element_by_id('submit-button').click()
        sleep(1)

    def tearDown(self):
        # todo:在此增加删除vote的代码
        self.browser.quit()

    def do_vote(self, questions):
        self.browser.find_element_by_id('homework-question-open').click()
        sleep(0.3)
        self.browser.find_elements_by_css_selector('#homework-question li a')[0].click()
        sleep(0.5)
        for num, element in enumerate(self.browser.find_elements_by_css_selector('.checkbox>div')):
            if num + 1 in questions:
                element.click()
        sleep(0.3)
        self.browser.find_element_by_class_name('btn').click()
        sleep(1)

    def add_tags(self):
        # 测试教师重新登录了网站
        self.login('functional_test_teacher', 'TDD is good')
        self.browser.get('http://localhost:8000/teacher/list/')
        sleep(0.3)
        self.browser.find_elements_by_class_name('vote-item')[0].click()
        sleep(1)
        list(map(lambda input_: input_[1].send_keys(input_[0]),
                 zip(('a b f ', 'b c f ', 'd ', 'e ', 'f ', 'g f '),
                     self.browser.find_elements_by_class_name('tag-inputbox'))))
        sleep(0.3)
        self.browser.find_element_by_id('button-submit').click()
        sleep(1)

    def start_a_vote(self):
        # 测试教师登录了网站
        self.login('functional_test_teacher', 'TDD is good')
        # 测试教师发起了Vote
        self.browser.get('http://localhost:8000/teacher/new-vote/')
        sleep(2)
        self.browser.find_element_by_id('name').send_keys('Vote for func_test1')
        start_date = self.browser.find_element_by_id('start-date')
        start_date.send_keys('2016')
        start_date.send_keys(Keys.TAB)
        start_date.send_keys('01')
        start_date.send_keys('01')
        sleep(0.3)
        end_date = self.browser.find_element_by_id('end-date')
        end_date.send_keys('2016')
        end_date.send_keys(Keys.TAB)
        sleep(0.3)
        end_date.send_keys('12')
        sleep(0.3)
        end_date.send_keys('31')
        Select(self.browser.find_element_by_css_selector('#class-choosed')).select_by_visible_text(
            '测试学校A 高一(1)班')
        Select(self.browser.find_element_by_css_selector('#class-choosed')).select_by_visible_text(
            '测试学校A 高一(2)班')
        sleep(0.3)
        self.browser.find_element_by_id('question-count').send_keys('22')
        self.browser.find_element_by_class_name('btn').click()
        sleep(1)


class TeacherTagInfoTest(TagInfoTest):
    def setUp(self):
        super(TeacherTagInfoTest, self).setUp()
        self.login('functional_test_teacher', 'TDD is good')

    def test_class_info(self):
        # 测试教师打开了Tag信息页面
        self.browser.get('http://localhost:8000/teacher/tag-info/')
        sleep(1)
        # 测试教师发现总体比较易错的知识点
        self.assertIn('a 3', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('b 6', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('c 3', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('d 2', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('f 10', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('g 2', self.browser.find_element_by_id('tag-list').text)
        sleep(0.3)

        # 测试教师选择了班级
        self.browser.find_element_by_class_name('dropdown-toggle').click()
        sleep(1)
        self.browser.find_elements_by_class_name('class-item')[0].click()
        sleep(1)
        # 测试教师发现班级比较易错的知识点
        self.assertIn('测试学校A 高一(1)班', self.browser.find_element_by_id('which-class-selected').text)
        self.assertIn('a 2', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('b 4', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('c 2', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('d 2', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('f 8', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('g 2', self.browser.find_element_by_id('tag-list').text)
        sleep(0.3)
        # 测试教师选择了班级
        self.browser.find_element_by_class_name('dropdown-toggle').click()
        sleep(1)
        self.browser.find_elements_by_class_name('class-item')[1].click()
        sleep(1)
        # 测试教师发现班级比较易错的知识点
        self.assertIn('测试学校A 高一(2)班', self.browser.find_element_by_id('which-class-selected').text)
        self.assertNotIn('d', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('b 2', self.browser.find_element_by_id('tag-list').text)
        sleep(0.3)

        self.browser.quit()


class StudentTagInfoTest(TagInfoTest):
    def setUp(self):
        super(StudentTagInfoTest, self).setUp()
        self.login('functional_test_student1', 'TDD is good')

    def test_class_info(self):
        # 测试学生打开了Tag信息页面
        self.browser.get('http://localhost:8000/student/tag-info/')
        sleep(1)
        # 测试学生发现了自己比较易错的知识点
        self.assertIn('a 1', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('b 2', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('c 1', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('d 1', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('f 4', self.browser.find_element_by_id('tag-list').text)
        self.assertIn('g 1', self.browser.find_element_by_id('tag-list').text)
