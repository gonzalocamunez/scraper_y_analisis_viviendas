import requests
from rich import print
import os

class Extractor:
    def __init__(self):
        self.session = requests.Session()
        self.proxy = os.getenv("mobileproxyuk")
        if self.proxy:
            self.session.proxies.update({"http": self.proxy, "https": self.proxy})

    def headers_from_browser(self, url):
        with Camoufox() as browser:
            page = browser.new_page()
            page.goto("https://******.com")

            def handle_request(request):
                global request_headers
                if "api" in request.url:
                    request_headers = request.headers
                    for k, v in request_headers.items():
                        if k.lower() not in [
                            "content-length",
                            "transfer-encoding",
                            "set-cookie",
                        ]:
                            self.session.headers.update({k: v})

            page.on("request", handle_request)
            page.goto(url)
            page.wait_for_load_state("networkidle")
            page.reload()
            page.wait_for_load_state("networkidle")
            browser.close()
            print("session headers", self.session.headers)

    def get(self, url):
        resp = self.session.get(url)
        return resp