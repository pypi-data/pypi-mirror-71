# coding="utf-8"
import requests
import json
import configparser
import time


class wechatntf():
    def __init__(self):
        self.url = "http://wxpusher.zjiecode.com/api/send/message"
        self.headers = {
            "Content-Type": "application/json"
        }

    def wechatsend(self, summary="", content="", contentType=1):
        """
        summary为消息概览，content为消息内容，
        contentType为消息类型：
        1表示文字
        2表示html(只发送body标签内部的数据即可，不包括body标签)
        3表示markdown
        """
        self.data = {
            "summary": summary,
            "content": content,
            "contentType": contentType
        }
        config = configparser.ConfigParser()
        # config.read('/usr/local/config.ini')
        config.read('config.ini')
        self.data["appToken"] = config["DEFAULT"]["appToken"]
        self.data["topicIds"] = json.loads(config['DEFAULT']['topicIds'])
        self.data = json.dumps(self.data)
        # print(self.data)
        i = 0
        while i < 5:
            try:
                requests.post(url=self.url, headers=self.headers, data=self.data,
                              timeout=5).content.decode()
                break
            except Exception as ret:
                print(str(ret))
                time.sleep(0.5)
                i += 1


if __name__ == '__main__':
    a = wechatntf()
    res = a.wechatsend(content="这是一条测试消息")
