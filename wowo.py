import os
from pathlib import Path
import requests_cache
from datetime import timedelta
import math


session = requests_cache.CachedSession(
    os.path.join(Path.home(), ".wowo", "cache"),
    backend="filesystem",
    expire_after=timedelta(days=30))


def get_response(url):
    response = session.get(url)
    response.raise_for_status()
    return response


def get_json(url):
    data = get_response(url).json()
    if "errno" in data:
        assert data["errno"] == 0, data["errmsg"]
    return data["data"]


def get_image(url):
    return get_response(url).content


URL_PREFIX = "https://app.woyouzhijia.cn/app/community"


def get_wowo_list():
    return get_json(f"{URL_PREFIX}/site/search/findBasicWoWo?latitude=39.799574&limit=1000&longitude=116.421593&page=1&range=20&type=true")


def get_wowo_detail(wowo_id):
    return get_json(f"{URL_PREFIX}/site/get?siteId={wowo_id}")


def get_wowo_comments(wowo_id):
    return get_json(f"{URL_PREFIX}/comment/findComment?limit=10&page=1&siteId={wowo_id}")


def bd09_to_gaode(lng, lat):
    '''
    百度坐标转高德坐标
    :param lng: 经度
    :param lat: 纬度
    :return:
    '''
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    x = lng - 0.0065
    y = lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y,x) - 0.000003 * math.cos(x * x_pi)
    lng_g = z * math.cos(theta)
    lat_g = z * math.sin(theta)
    return lng_g, lat_g
