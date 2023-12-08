import requests
import json
from requests.exceptions import Timeout, RequestException


def check_update(url, app_name, current_version) -> int:
    result = 0
    try:
        response = requests.get(url + "update.json", timeout=5)
        try:
            response.raise_for_status()  # 如果返回状态码不是200，则抛出异常
        except requests.exceptions.HTTPError as e:
            print(f"获取更新文件: {e.response.status_code}")
            return result
    except Timeout:
        print("获取更新文件请求超时")
        return result
    except RequestException as e:
        print(f"获取更新文件请求发生错误 {e}")
        return result
    update_json: dict = json.loads(response.text)
    data: dict = update_json.get(app_name)
    web_version = data.get("version")
    if web_version and web_version > current_version:
        result = web_version
    return result
