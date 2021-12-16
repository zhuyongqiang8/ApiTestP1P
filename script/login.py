import logging
import unittest
from time import sleep

import requests
from api.loginAPI import LoginAPI
import random
from utils import assert_utils


class login(unittest.TestCase):
    phone1 = '13033447767'
    phone2 = '13033447725'
    phone3 = '13033447744'
    phone4 = '13033447677'
    pwd = 'test123'
    imgCode = '8888'
    smsCode = '666666'

    def setUp(self) -> None:
        self.login_api = LoginAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 参数为随机小数时获取图片验证码成功
    def test01_get_img_code_random_float(self):
        # 定义获取随机小数
        r = random.random()
        # 调用接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口返回断言
        self.assertEqual(200, response.status_code)

    # 参数为随机整数时获取图片验证码成功
    def test02_get_img_code_random_int(self):
        # 定义参数（随机整数）
        r = random.randint(1000000, 9000000)
        # 调用接口类中的发送图片验证码接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，并进行断言
        self.assertEqual(200, response.status_code)

    # 参数为空，获取图片验证码失败
    def test03_get_img_code_param_is_null(self):
        # 定义参数（随机整数）
        # 调用接口类中的发送图片验证码接口
        response = self.login_api.getImgCode(self.session, "")
        # 接收接口的返回结果，并进行断言
        self.assertEqual(404, response.status_code)

    # 参数为随机字母时，获取图片验证码失败
    def test04_get_img_code_random_char(self):
        # 定义参数（随机整数）
        r = random.sample("asdfghjqwertyuizxcvbnm", 8)
        dan = ''.join(r)
        # 调用接口类中的发送图片验证码接口
        response = self.login_api.getImgCode(self.session, dan)
        # 接收接口的返回结果，并进行断言
        self.assertEqual(400, response.status_code)

        # 获取短信验证码成功——参数正确

    def test05_get_sms_code_success(self):
        # 定义获取随机小数
        r = random.random()
        # 调用接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口返回断言
        self.assertEqual(200, response.status_code)
        # 调用接口类中的发送图片验证码接口
        resronse = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        # 接收接口的返回结果，并进行断言
        assert_utils(self, resronse, 200, 200, "短信发送成功")

    # 获取短信验证码失败—图片验证码错误
    def test06_get_sms_code_wrong_img_code(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 定义错误验证码
        error_code = '1234'
        # 调用接口类中的发送图片验证码接口
        response = self.login_api.getSmsCode(self.session, self.phone1, error_code)
        # 接收接口的返回结果，并进行断言
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 获取短信验证码失败——图片验证码为空
    def test07_get_sms_code_img_code_is_null(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 发送短信验证码接口
        # 调用接口类中的接口
        response = self.login_api.getSmsCode(self.session, self.phone1, '')
        # 接收接口的返回结果，进行断言
        assert_utils(self, response, 200, 100, '图片验证码错误')

        # 获取短信验证码失败——手机号为空

    def test08_get_sms_code_phone_is_null(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 接收接口的返回结果，进行断言

        # 2、发送短信验证码
        # 定义参数（手机号为空，验证码正确）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, '', self.imgCode)
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

    # 获取短信验证码失败——未调用获取图片验证码错接口
    def test09_get_sms_code_no_img_Verify(self):
        # 1、未获取图片验证码
        # 2、获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 输入必填项，注册成功
    def test10_register_success_param_must(self):
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        respopse = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, respopse.status_code)
        # 调用接口类中的接口
        response = self.login_api.getSmsCode(self.session, self.phone2, self.imgCode)
        # 接收接口的返回结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 调用接口类中的接口
        response = self.login_api.register(self.session, self.phone2, self.pwd)
        # 调用接口类中的发送短信验证码的接口
        assert_utils(self, response, 200, 200, "注册成功")

    # 输入所有项，注册成功
    def test11_register_success_param_all(self):
        # 定义获取随机小数
        r = random.random()
        # 调用接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口返回断言
        self.assertEqual(200, response.status_code)
        # 调用接口类中的发送图片验证码接口
        resronse = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        # 接收接口的返回结果，并进行断言
        assert_utils(self, resronse, 200, 200, "短信发送成功")
        # 发送注册请求
        response = self.login_api.register(self.session, self.phone1, self.pwd, invite_phone='13012345678')
        # 进行结果并断言
        assert_utils(self, response, 200, 200, "注册成功")

    # 手机号已存在时，注册失败
    def test12_register_phone_is_exist(self):
        # 1、成功获取图片验证码
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册失败——手机号以重复
        # 调用接口类中的发送注册请求的接口
        response =self.login_api.register(self.session,self.phone1,self.pwd)
        # 接收接口的返回结果，进行断言
        assert_utils(self,response,200,100,"手机已存在!")

    # 注册失败——密码为空
    def test13_register_password_is_null(self):
        # 1、成功获取图片验证码
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone3, self.imgCode)
        # 对接收的相应断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册失败——手机号以重复
        # 调用接口类中的发送注册请求的接口
        response =self.login_api.register(self.session,self.phone3,'')
        # 接收接口的返回结果，进行断言
        assert_utils(self,response,200,100,"密码不能为空")

    # 注册失败——图片验证码错误
    def test14_register_img_code_is_wrong(self):
        # 1、成功获取图片验证码
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone3, self.imgCode)
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册失败——图片验证码错误
        # 调用接口类中的发送注册请求的接口
        response =self.login_api.register(self.session,self.phone3,self.pwd,'1234')
        # 接收接口的返回结果，进行断言
        assert_utils(self,response,200,100,"验证码错误!")

    # 注册失败——短信验证码错误
    def test15_register_sms_code_is_wrong(self):
        # 1、成功获取图片验证码
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone4, self.imgCode)
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册失败——短信验证码错误
        # 调用接口类中的发送注册请求的接口
        response =self.login_api.register(self.session,self.phone4,self.pwd,'1234')
        # 接收接口的返回结果，进行断言
        assert_utils(self,response,200,100,"验证码错误!")

        # 注册失败——不同注册协议
    def test16_register_no_agree_protocol(self):
        # 1、成功获取图片验证码
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone4, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册失败——不同意注册协议
        # 调用接口类中的发送注册请求的接口
        response =self.login_api.register(self.session,self.phone4,self.pwd,dyServer='off')
        # 接收接口的返回结果，进行断言
        assert_utils(self,response,200,100,"请同意我们的条款")

        # 登录成功

    def test17_login_success(self):
        # 准备参数
        # 调用接口类中的发送登录的接口
        response =self.login_api.login(self.session,self.phone1,self.pwd)
        # 接收接口的返回结果，进行断言
        assert_utils(self,response,200,200,"登录成功")

    # 登录失败——用户名不存在
    def test18_login_phone_not_exist(self):
        # 准备参数
        Wphone = '13000000000'
        # 调用接口类中的发送登录的接口
        response =self.login_api.login(self.session,Wphone,self.pwd)
        # 接收接口的返回结果，进行断言
        assert_utils(self,response,200,100,"用户不存在")

    # 登录失败——密码为空
    def test19_login_pwd_is_null(self):
        # 调用接口类中的发送登录的接口
        response =self.login_api.login(self.session,self.phone1,"")
        # 接收接口的返回结果，进行断言
        assert_utils(self, response, 200, 100, "密码不能为空")

    # 登录失败——密码错误
    def test20_login_wrong_pwd(self):
        #定义错误密码
        wrong_pwd = 'error'
        # 调用接口类中的发送登录的接口
        response =self.login_api.login(self.session,self.phone2,wrong_pwd)
        # 接收接口的返回结果，进行断言
        assert_utils(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")
        # 调用接口类中的发送登录的接口
        response =self.login_api.login(self.session,self.phone2,wrong_pwd)
        # 接收接口的返回结果，进行断言
        assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")
        response =self.login_api.login(self.session,self.phone2,wrong_pwd)
        # 接收接口的返回结果，进行断言
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        # 4、输入正确密码，提示被锁定
        response = self.login_api.login(self.session, self.phone2,self.pwd)
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        # 5、等待60s，再输入正确密码，提示登录成功
        sleep(60)
        response =self.login_api.login(self.session,self.phone2,self.pwd)
        # 接收接口的返回结果，进行断言
        assert_utils(self,response,200,200,"登录成功")





















