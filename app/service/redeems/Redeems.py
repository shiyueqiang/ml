# coding:utf-8
# Author：lxm
from app.utils.requester import requester
from app.utils.common import tools
from app.config.pathconfig import *
import os
import json

modelName = "redeems"
config = tools.get_config(os.path.join(configPath, "config.ini"))


def createRedeemsOrder(redeemsType, pId, money, isWhole, token):
    payload = tools.get_json(os.path.join(dataPath, modelName, "createRedeemsOrder.json"))
    payload["fun"]["createRedeemOrder"]["redeemType"] = redeemsType
    payload["fun"]["createRedeemOrder"]["pId"] = pId
    payload["fun"]["createRedeemOrder"]["money"] = money
    payload["fun"]["createRedeemOrder"]["isWhole"] = isWhole
    payload["statics"]["token"] = token
    url = config["api"]["xwapi"]
    res = requester.post_template(url=url, payload=json.dumps(payload))
    if json.loads(res)["createRedeemOrder"]["error_code"] != 0:
        tools.log().error("error ---------- 创建转出订单失败！")
    return json.loads(res)["createRedeemOrder"]["data"]["orderId"]


def sureRedeemOrder(orderId, token):
    payload = tools.get_json(os.path.join(dataPath, modelName, "sureRedeemOrder.json"))
    payload["fun"]["sureRedeemOrder"]["orderId"] = orderId
    payload["statics"]["token"] = token
    url = config["api"]["xwapi"]
    res = requester.post_template(url=url, payload=json.dumps(payload))
    if json.loads(res)["sureRedeemOrder"]["error_code"] != 0:
        tools.log().error("error ---------- 确认转出订单失败！")


if __name__ == '__main__':
    orderId = createRedeemsOrder(1, 24, 2, 0, "da3194e62c53d69cf9bbe41674ace239")
    sureRedeemOrder(orderId, "da3194e62c53d69cf9bbe41674ace239")
