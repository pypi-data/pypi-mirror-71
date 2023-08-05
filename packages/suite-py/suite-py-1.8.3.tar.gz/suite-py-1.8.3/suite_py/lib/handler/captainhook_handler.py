# -*- encoding: utf-8 -*-
import sys
import requests

from suite_py.lib.config import Config
from suite_py.lib.singleton import Singleton
from suite_py.lib.handler import git_handler as git
from suite_py.lib.logger import Logger

config = Config()
logger = Logger()


class CaptainHook(metaclass=Singleton):
    _baseurl = None
    _timeout = None

    def __init__(self):
        self._baseurl = config.load()["user"]["captainhook_url"]
        self._timeout = config.load()["user"]["captainhook_timeout"]

    def lock_project(self, project, env):
        data = {
            "project": project,
            "status": "locked",
            "user": git.get_username(),
            "environment": env,
        }
        return self.send_post_request("/projects/manage-lock", data)

    def unlock_project(self, project, env):
        data = {
            "project": project,
            "status": "unlocked",
            "user": git.get_username(),
            "environment": env,
        }
        return self.send_post_request("/projects/manage-lock", data)

    def status(self, project, env):
        return self.send_get_request(
            f"/projects/check?project={project}&environment={env}"
        )

    def check(self):
        return requests.get(f"{self._baseurl}/", timeout=(2, self._timeout))

    def get_users_list(self):
        return self.send_get_request("/users/all")

    def rollback(self, project, version):
        data = {
            "project": project,
            "user": git.get_username(),
            "version": version,
        }
        return self.send_post_request("/projects/rollback", data)

    def send_post_request(self, endpoint, data):
        try:
            return requests.post(
                f"{self._baseurl}{endpoint}", data=data, timeout=self._timeout
            )
        except Exception:
            logger.error("Impossibile contattare CaptainHook, stai usando la VPN?")
            sys.exit(-1)

    def send_get_request(self, endpoint):
        try:
            return requests.get(
                f"{self._baseurl}{endpoint}", timeout=(2, self._timeout)
            )
        except Exception:
            logger.error("Impossibile contattare CaptainHook, stai usando la VPN?")
            sys.exit(-1)

    def set_timeout(self, timeout):
        self._timeout = timeout
