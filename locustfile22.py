from locust import task, run_single_user
from locust import FastHttpUser


class chrome20241122(FastHttpUser):
    host = "http://10.50.11.120:9001"
    default_headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "10.50.11.120:9001",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    }

    @task
    def t(self):
        with self.rest(
            "POST",
            "/api/uims/login",
            headers={
                "Content-Length": "183",
                "Origin": "http://10.50.11.120:9001",
                "token": "null",
            },
            json={
                "systemName": "ifood-operating-manage",
                "authenType": 1,
                "password": "123456",
                "phoneNumber": "18930410921",
                "smsCode": None,
                "kaptchaCode": "1",
                "kaptchaKey": "2e3da65159924ad3acbabd93f9fb3186",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "/api/uims/queryUserOrg",
            headers={"token": "14291EA46E74C326D2BAE940201F055D"},
        ) as resp:
            pass
        with self.rest(
            "POST",
            "/api/base/org/config/queryConfig",
            headers={
                "Content-Length": "87",
                "Origin": "http://10.50.11.120:9001",
                "token": "14291EA46E74C326D2BAE940201F055D",
            },
            json={
                "modelCode": "merchant_dsp_config",
                "organizationId": "2021040701",
                "organizationType": 22,
            },
        ) as resp:
            pass
        with self.rest(
            "POST",
            "/api/sales/mer/si/getTips",
            headers={
                "Content-Length": "2",
                "Origin": "http://10.50.11.120:9001",
                "token": "14291EA46E74C326D2BAE940201F055D",
            },
            json={},
        ) as resp:
            pass
        with self.rest(
            "POST",
            "/api/mer/store/queryPage",
            headers={
                "Content-Length": "72",
                "Origin": "http://10.50.11.120:9001",
                "token": "14291EA46E74C326D2BAE940201F055D",
            },
            json={
                "pageNum": 1,
                "pageSizeZero": True,
                "pageSize": 0,
                "merchantId": "2021040701",
            },
        ) as resp:
            pass

        with self.rest(
            "POST",
            "/api/mer/merchants/queryPage",
            headers={
                "Content-Length": "46",
                "Origin": "http://10.50.11.120:9001",
                "token": "14291EA46E74C326D2BAE940201F055D",
            },
            json={"pageNum": 1, "pageSize": 0, "pageSizeZero": True},
        ) as resp:
            pass
        with self.rest(
            "POST",
            "/api/query/userInfos",
            headers={
                "Content-Length": "147",
                "Origin": "http://10.50.11.120:9001",
                "token": "14291EA46E74C326D2BAE940201F055D",
            },
            json={
                "userBackStatus": "0",
                "phoneNumber": "",
                "nickName": "",
                "memberCard": "",
                "merchantId": "2021040701",
                "pageNum": 1,
                "delFlag": 0,
                "pageSize": 10,
                "sysId": "iom",
            },
        ) as resp:
            pass
        with self.rest(
            "POST",
            "/api/mer/merchants/queryPage",
            headers={
                "Content-Length": "46",
                "Origin": "http://10.50.11.120:9001",
                "token": "14291EA46E74C326D2BAE940201F055D",
            },
            json={"pageNum": 1, "pageSize": 0, "pageSizeZero": True},
        ) as resp:
            pass
        with self.rest(
            "POST",
            "/api/faceAi/getUserInfos",
            headers={
                "Content-Length": "162",
                "Origin": "http://10.50.11.120:9001",
                "token": "14291EA46E74C326D2BAE940201F055D",
            },
            json={
                "pageNum": 1,
                "pageSize": 10,
                "delFlag": 0,
                "departmentName": "",
                "merchantName": "",
                "merchantId": "2021040701",
                "cooperativeMerchantId": "",
                "dimission": "",
                "phoneNumber": "",
            },
        ) as resp:
            pass


if __name__ == "__main__":
    run_single_user(chrome20241122)
