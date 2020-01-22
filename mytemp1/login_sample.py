# -*- coding: utf-8 -*-
# __author__ = 'lusn'
#注册用户+模块化+数据驱动，实现所有注册，测试用例 selenium
import time
import unittest
from selenium import webdriver
import random
from selenium.webdriver.common.action_chains import ActionChains
'''
class LoginTest(unittest.TestCase):
    '''注册'''
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def test_login(self):
        driver=self.driver
        driver.get("http://testing-www.intranet.dcml.com/home")
        #区号选择
        double_click=driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[1]/div/div")
        ActionChains(driver).double_click(double_click).perform()
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[1]/div/ul/li[1]/div").click()#KR  li[1]CN  li[2]US li[3]
        #手机号
        #driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[2]/div[2]/input").send_keys("15009990361")

        list=["130","131","132","133","134","135","136","137","138","139","147","150","151","152","153","155","156","157","158","159","186","187","188"]
        shou=( random.choice(list))
        wo=str(random.randint(00000000,99999999))
        wei=wo.zfill(8)
        tel=shou+wei
        print(tel)
        driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[2]/div[2]/input").send_keys(tel)

        #密码
        driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[3]/div[2]/input").send_keys("11111111")
        #重复密码
        driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[4]/div[2]/input").send_keys("11111111")
        #验证码
        driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[5]/div[2]/div/div/button").click()
        driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[5]/div[2]/div/input").send_keys("123456")
        #协议
        '''
        driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[6]/div[1]/img").click()
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/
        orm/div[6]/div[1]/img").click()
        '''
        #提交
        driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[7]/button").click()

        # title=driver.title
        # self.assertEqual(title,"Coin&Cash - 数字货币抵押贷款-基于智能合约打造的数字资产抵押贷款平台") #断言
        # print(title)

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
'''

class game_login():
