# coding:utf-8
# Author：lxm
from app.utils.requester import requester
from app.utils.common import tools
from app.config.pathconfig import *
import os
import json

modelName = "product"
config = tools.get_config(os.path.join(configPath, "config.ini"))


# 获取指定产品当前正在开标的标的 返回标的信息
def oneProductDetail(token, pId):
    bTypeDict = {12: 0, 24: 3, 25: 3, 26: 3, 29: 5, 35: 6}
    payload = tools.get_json(os.path.join(dataPath, modelName, "oneProductDetail.json"))
    payload["token"] = token
    payload["pId"] = pId
    payload["bType"] = bTypeDict[pId]
    url = config["api"]["xwm_url"] + config["api"]["one_product_detail"]
    res = requester.get_template(url=url, payload=payload)
    if json.loads(res)["data"]["product"]["bId"] == "":
        tools.log().error("当前产品暂无可用标的！--pId：%d" % pId)
        return None
    return json.loads(res)["data"]["product"]


if __name__ == '__main__':
    oneProductDetail('a70c18342f8be2d3280c797639b1c7b8', 24)
