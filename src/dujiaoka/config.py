import os

from .requests import getSession
from .log import Log

logger = Log(__name__).getlog()


class Config:
    def __init__(self):
        self.base_url = (
            os.getenv("DUJIAO_BASE_URL").rstrip("/") + "/"
            if os.getenv("DUJIAO_BASE_URL")
            else None
        )
        self.username = os.getenv("DUJIAO_USERNAME")
        self.password = os.getenv("DUJIAO_PASSWORD")

        if not (self.base_url and self.username and self.password):
            exit(
                "Please set the environment variables DUJIAO_BASE_URL, DUJIAO_USERNAME and DUJIAO_PASSWORD"
            )

        self.session_name = "dujiao_session.pkl"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        }

        self.session = getSession(base_url=self.base_url)
        self.session.headers.update(self.headers)

    def login(self):
        logger.info(f"[+] Logging in to {self.base_url}")

        html_login = self.session.get("/auth/login").text
        if "欢迎回来，请登录您的账号" not in html_login:
            logger.info("[+] Trial Login Success")
            return True

        logger.info("[+] Trial Login Failed")
        if 'name="_token" value="' not in html_login:
            logger.error("[-] Token not found")
            return False

        # Get CSRF token
        token = html_login.split('name="_token" value="')[1].split('"')[0]
        logger.debug("[+] Token: " + token)

        res = self.session.post(
            "/auth/login",
            data={
                "username": self.username,
                "password": self.password,
                "_token": token,
                "remember": "1",
            },
        )

        status = res.json()
        if status["status"]:
            logger.info("[+] Login Successful")

            return True

        logger.error("[-] Login Failed")
        return False


config = Config()
