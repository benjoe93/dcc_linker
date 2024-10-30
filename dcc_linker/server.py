import json
import queue
import sys
import threading
import time
import urllib.parse as parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable

import requests

from . import apps
from .constants import HostApps


class MainThreadManager:
    """
    This class is responsible for managing and executing function on the main thread
    """

    def __init__(self, app: str = ""):
        self.task_queue = queue.Queue()
        self.app = app

        self.__loaded_modules = []

    def main_thread_poller(self) -> float:
        """
        Responsible to periodically check and handle task in the queue

        Returns:
            float: the time between iterations. Currently tested with Blender's *bpy.app.timers.register()*
        """

        while self.task_queue:
            # get the function name and parameters from the server
            try:
                func_name, params = self.task_queue.get_nowait()
                print(func_name, params)
                # execute
                self.try_to_execute_function(func_name, params)
            except queue.Empty:
                break
        return 0.5

    def try_to_execute_function(self, function_name: str, parameters: dict):
        func: Callable = self.find_function_by_name(function_name, self.app)
        func(**parameters)

    def find_function_by_name(self, function_name: str, app_name: str = None) -> Callable:
        if app_name is not None:
            with open(r"D:\dev\unreal\ToolsTest\Plugins\WebHook\Content\Python\log.json", "w") as f:
                m = [f"{m}\n" for m in sys.modules]
                f.write(json.dumps(m, indent=4))

            module = sys.modules.get(f"dcc_linker.apps.{app_name}")
            if module is not None:
                modules_lst = [module]
            else:
                module = sys.modules.get(app_name)
                modules_lst = [module]
        else:
            modules_lst = self.__loaded_modules

        for module in modules_lst:
            print(module)
            for name, value in module.__dict__.items():
                if callable(value):
                    if function_name == name:
                        return value


class Server(HTTPServer):
    """Base server class"""

    def __init__(
        self,
        server_address,
        RequestHandlerClass,
        bind_and_activate=True,
        main_manager: MainThreadManager = None,
    ) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.main_manager: MainThreadManager = main_manager

    def start_server(self) -> None:
        print(f"SERVER IS RUNNING on port: {self.server_port}")
        self.serve_forever()
        self.server_close()
        print("BYE BYE!")

    def start_server_on_thread(self) -> threading.Thread:
        print("Starting....")
        t = threading.Thread(target=self.start_server, daemon=True)
        t.start()
        return t


class DccRequestHandler(BaseHTTPRequestHandler):
    "Base HTTP Request Handler"
    server: "Server"

    def do_GET(self) -> None:

        if self.path == "/favicon.ico":
            return

        func_name, params = self.parse_get_data(self.path)
        print(func_name)
        print(params)
        payload: dict[str, str] = {
            "objectPath": "/Engine/PythonTypes.Default__WebFuncLib",
            "functionName": func_name,
            "parameters": params,
            "generateTransaction": "true",
        }
        print(payload)

        ue_repsonse = self.send_to_unreal(payload)
        print(f"[UNREAL] {ue_repsonse.status_code}:  {ue_repsonse.json()}")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # closes the browser tab
        self.wfile.write(
            bytes(
                "<script type='text/javascript'>window.open('', '_self', ''); window.close();</script>".encode("utf-8")
            )
        )
        # page blocks server! WHY??

    def do_POST(self) -> None:
        # receive and decode the payload
        content_length = int(self.headers["Content-Length"])
        raw_data: str = self.rfile.read(content_length).decode("utf-8")
        print(raw_data)
        if not raw_data:
            print("No incoming data found!")
            return

        post_data: dict = json.loads(raw_data)

        # get the function name and the parameter dict out from the json payload coming in
        func_name: str = post_data.get("func", "")
        params: dict[str, str] = post_data.get("params", {})

        # add task to main thread queue
        if manager := self.server.main_manager:
            manager.task_queue.put((func_name, params))

        # send response
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def parse_get_data(self, path: str) -> tuple[str, dict[str, str]]:
        """Parses data from the GET request

        Args:
            path (str): content of the request query

        Returns:
            tuple[str, dict[str, str]]: Function name, parameters dictionary
        """

        data: str = parse.unquote(path).lstrip("/?")
        parts: list[str] = data.split("&")
        func_name: str = parts[0]
        try:
            in_params: str = parts[1]
            params: dict[str, str] = json.loads(in_params)
        except Exception as e:
            print(e)

        return func_name, params

    def send_to_unreal(self, payload) -> requests.Response:
        headers: dict[str, str] = {"Content-Type": "application/json"}

        return requests.request(
            "PUT",
            "http://localhost:30010/remote/object/call",
            data=json.dumps(payload),
            headers=headers,
        )
