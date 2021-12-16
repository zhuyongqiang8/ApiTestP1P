import unittest

import requests

from api.loginAPI import LoginAPI
from api.trustAPI import trustAPI
from utils import assert_utils


class tender(unittest.TestCase):
    tender_id = 697

    def setUp(self) -> None:
        self.login_api = LoginAPI()
        self.tender_api = trustAPI()
        self.session = requests.Session()
        # 登录成功
        respsonse=self.login_api.login(self.session)
        # 接收接口的返回结果，并进行断言
        assert_utils(self,respsonse,200,200,"登录成功!")

    def tearDown(self) -> None:
        self.session.close()

    def test01_get_loaninfo(self):
        """获取投资产品详情"""
        # 请求投资产品的详情