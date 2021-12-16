import unittest

import requests
from utils import assert_utils
from api.approveAPI import approveAPI
from api.loginAPI import LoginAPI


class approve(unittest.TestCase):
    phone1 = '13033447711'
    phone2 = '13033447712'
    realname = '张三'
    cardId = '110117199003070995'

    def setUp(self) -> None:
        self.login_api = LoginAPI()
        self.approve_api = approveAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 认证成功
    def test01_approve_success(self):
        # 用户登录
        response = self.login_api.login(self.session)
        # 接收接口的返回结果，进行断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、发送认证请求
        # 准备参数
        # 调用接口脚本中定义的方法发送请求
        response = self.approve_api.approve(self.session, self.realname, self.cardId)
        # 接收接口的返回结果，进行断言
        assert_utils(self, response, 200, 200, "提交成功!")

    # 认证失败——姓名为空
    def test02_approve_realname_is_null(self):
        # 1、用户登录
        response = self.login_api.login(self.session, self.phone2)
        # 接收接口的返回结果，进行断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、发送认证请求 _ 姓名为空
        # 准备参数
        # 调用接口脚本中定义的方法发送请求
        response = self.approve_api.approve(self.session, "", self.cardId)
        # 接收接口的返回结果，进行断言
        assert_utils(self, response, 200, 100, "姓名不能为空")

    # 认证失败——身份证号为空
    def test03_approve_cardId_is_null(self):
        # 1、用户登录
        response = self.login_api.login(self.session, self.phone2)
        # 接收接口的返回结果，进行断言
        assert_utils(self,response,200,200,"登录成功")
        # 2、发送认证请求 _ 姓名为空
        # 准备参数
        # 调用接口脚本中定义的方法发送请求
        response =self.approve_api.approve(self.session,self.realname,"")
        # 接收接口的返回结果，进行断言
        assert_utils(self, response, 200, 100, "身份证号不能为空")

     # 获取认证信息
    def test04_get_approve(self):
        #   1、用户登录
        response = self.login_api.login(self.session, self.phone1)
        # 接收接口的返回结果，进行断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、获取认证请求
        response =self.approve_api.getApprove(self.session)
        # 接收接口的返回结果，进行断言
        self.assertEqual(200,response.status_code)