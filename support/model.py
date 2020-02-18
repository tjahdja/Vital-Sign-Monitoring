import urllib.request
import time


class Model:
    def __init__(self):
        super().__init__()

    def comm(self, comport):
        try:
            self.url = f"http://{comport}/Python"
            self.rawdata = urllib.request.urlopen(self.url).read()
            self.rawdata = self.rawdata.decode("utf-8")
            time.sleep(1)
        except Exception as e:
            print(e)