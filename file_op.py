import requests
import json
import os
from print_info import *


def download_json(json_path):
    json_url = "https://api.hearthstonejson.com/v1/latest/zhCN/cards.json"
    file = requests.get(json_url)

    with open(json_path, "wb") as f:
        f.write(file.content)


def read_json():
    dir_path = os.path.dirname(__file__)
    if dir_path == "":
        dir_path = "."
    json_path = dir_path + "/cards.json"

    if not os.path.exists(json_path):
        sys_print("未找到cards.json,试图通过网络下载文件")
        download_json(json_path)
    else:
        sys_print("cards.json已存在")

    with open(json_path, "r", encoding="utf8") as f:
        json_string = f.read()
        return json.loads(json_string)


if __name__ == "__main__":
    read_json()
