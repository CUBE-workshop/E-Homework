import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ClassInfoTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def login(self, username, password):
        self.browser.get('http://localhost:8000/sign-in/')
        sleep(1)
        self.browser.find_element_by_id('username').send_keys(username)
        self.browser.find_element_by_id('password').send_keys(password)
        sleep(3)
        self.browser.find_element_by_id('submit-button').click()
        sleep(1)

    def test_class_info(self):
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
        self.browser.find_elements_by_css_selector('#class-choosed > option')[0].click()
        self.browser.find_element_by_id('question-count').send_keys('22')
        self.browser.find_element_by_class_name('btn').click()
        sleep(1)
        # 测试学生1登录了网站
        self.login('functional_test_student1', 'TDD is good')
        # 测试学生1做了Vote（1，2，3，5，7，9，11，22）
        self.browser.find_element_by_id('homework-question-open').click()
        sleep(0.3)
        self.browser.find_elements_by_css_selector('#homework-question li a')[0].click()
        sleep(0.5)
        for num, element in enumerate(self.browser.find_elements_by_css_selector('.checkbox>div')):
            if num + 1 in [1, 2, 3, 5, 7, 9, 11, 22]:
                element.click()
        sleep(0.3)  #
        self.browser.find_element_by_class_name('btn').click()
        sleep(1)
        # 测试学生2登录了网站
        self.login('functional_test_student2', 'TDD is good')
        # 测试学生2做了Vote [1, 2, 3, 5, 4, 9, 22]
        self.browser.find_element_by_id('homework-question-open').click()
        sleep(0.3)
        self.browser.find_elements_by_css_selector('#homework-question li a')[0].click()
        sleep(0.5)
        for num, element in enumerate(self.browser.find_elements_by_css_selector('.checkbox>div')):
            if num + 1 in [1, 2, 3, 5, 4, 9, 22]:
                element.click()
        sleep(0.3)
        self.browser.find_element_by_class_name('btn').click()
        sleep(1)

        # 测试教师重新登录了网站
        self.login('functional_test_teacher', 'TDD is good')
        # 测试教师给Vote添加了Tag(a,b,c,d,e,f)

        # 测试教师打开了班级信息页面
        # 测试教师发现班级比较易错的知识点
        self.fail("这个测试还没有编写完成！")
